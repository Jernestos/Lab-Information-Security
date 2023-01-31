import sys
import os

'''
arch     x86
baddr    0x400000
binsz    1021210
bintype  elf
bits     64
canary   true
class    ELF64
compiler GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
crypto   false
endian   little
havecode true
laddr    0x0
lang     c
linenum  true
lsyms    true
machine  AMD x86-64 architecture
maxopsz  16
minopsz  1
nx       true
os       linux
pcalign  0
pic      false
relocs   true
rpath    NONE
sanitiz  false
static   true
stripped false
subsys   linux
va       true
'''

'''
magicbeans.txt

main:
12025: E:0x4012b7:C:19b:mov rbp, rsp 
12026: E:0x4012ba:C:31b:sub rsp, 0x60 

check_password:
14021: E:0x4011b5:C:19b:mov rbp, rsp 
14022: E:0x4011b8:C:31b:sub rsp, 0x40

E:0x4011bc:C:19b:mov qword ptr [rbp-0x28], rdi (password string pointer)
W:0x7ffd2f27fb28:D
E:0x4011c0:C:19b:mov dword ptr [rbp-0x2c], esi (password string length)
W:0x7ffd2f27fb24:D
E:0x4011c3:C:19b:mov qword ptr [rbp-0x38], rdx (password attempt string pointer)
W:0x7ffd2f27fb18:D
E:0x4011c7:C:19b:mov dword ptr [rbp-0x30], ecx (password attempt string length)


14037: E:0x4011d4:C:19b:mov dword ptr [rbp-0x8], eax (radare2: it's var_4h [rbp-0x4])
W:0x7ffd2f27fb48:D
E:0x4011d7:C:19b:mov dword ptr [rbp-0x14], 0x0 (radare2: it's  [rbp-0x10])
W:0x7ffd2f27fb3c:D
E:0x4011de:C:19b:mov dword ptr [rbp-0xc], 0x0 (radare2: it's  [rbp-0x8])
W:0x7ffd2f27fb44:D
E:0x4011e5:C:19b:mov byte ptr [rbp-0x1], 0x0 (radare2: it's  [rbp-0x11])
W:0x7ffd2f27fb4f:D
E:0x4011e9:C:19b:mov dword ptr [rbp-0x14], 0x0 (radare2: it's  [rbp-0x10])


14047: E:0x4011f0:C:12f:jmp 0x40128c  (in radare2 it's 0x401e27; offset by 2971 [0xb9b])


int max_length = MIN(p_size, i_size);
E:0x4011ca:C:19b:mov eax, dword ptr [rbp-0x2c] 
R:0x7ffd2f27fb24:D
E:0x4011cd:C:64:cmp dword ptr [rbp-0x30], eax 
R:0x7ffd2f27fb20:D
E:0x4011d0:C:57:cmovle eax, dword ptr [rbp-0x30] //eax = max_length

radare2 <-> trace translation
var_38h = var_38h //rdx (password attempt string pointer)
var_30h = var_30h //ecx (password attempt string length)
var_2ch = var_2ch // rsi - (password string length)
var_28h = var_28h //rdx - (password string pointer)
var_11h = [rbp-0x1]
var_10h = [rbp-0x14] //pos
var_ch = [rbp-0x10] //j (in else branch)
var_8h = [rbp-0xc] //k
var_4h = [rbp-0x8] //max_length

eax: max_length



Loop body check: pos < max_length
E:0x40128c:C:19b:mov eax, dword ptr [rbp-0x14] 
R:0x7ffd2f27fb3c:D
E:0x40128f:C:64:cmp eax, dword ptr [rbp-0x8] 
R:0x7ffd2f27fb48:D
E:0x401292:C:12d:jl 0x4011f5 



E:0x401211:C:8:add dword ptr [rbp-0xc], 0x1 <-> k++;
E:0x4012a8:C:19b:mov eax, 0x1 				<-> return 1;

'''

'''
E:0x401211: k++;
0x401217 (else branch if not same character)



E:0x4012a8:C:19b:mov eax, 0x1
E:0x4012af:C:19b:mov eax, 0x0 

'''


for_loop_pw_length_check = "E:0x4011f5" #pos < max_length
if_branch = "E:0x401211" # k++;
else_branch = "E:0x401217" #start of else
pow_address = "E:0x401450" #start address of pow
#end of pow: E:0x4014a6
distance_less_0 = "E:0x40126f" #+26
j_minus_1 = "E:0x40127e" #j--

pw_length_neq = "E:0x4012af" #goes to setting return value to 0 (return0) (branch for p_size != i_size)
pw_length_eq = "E:0x4012a0" #go to next check (k == p_size)

return0 = "E:0x4012af" #return 0;
return1 = "E:0x4012a8" #return 1; //also for k == p_size

#https://reverseengineering.stackexchange.com/questions/2774/what-does-the-assembly-instruction-repne-scas-byte-ptr-esedi
scan_password_attempt = "E:0x4013a9" #read from argument; account for null byte
scan_password = "E:0x4013de" #read from file password.txt; account for null byte


def analyse_trace(trace, password_attempt):
	
	password_reconstructed = ""
	
	password_attempt_length = -1 #sanity check; null byte
	password_length = -1 #sanity check; null byte
	
	current_index = -1 #offset (consider when we have not even entered loop)
	
	current_distance_less_0_bool = False
	
	current_distance = 0
	
	status = 0
	
	earlier_termination = False
	
	for current_trace_line in trace:
		
		#password length
		if scan_password in current_trace_line: #true password, verified
			password_length = password_length + 1
		
		#attempted password length
		if scan_password_attempt in current_trace_line: #attempted password, verified
			password_attempt_length = password_attempt_length + 1
		
		#loop check case
		if for_loop_pw_length_check in current_trace_line:
			current_index = current_index + 1
		
		#if case
		if if_branch in current_trace_line: #verified
			password_reconstructed = password_reconstructed + password_attempt[current_index]
		
		#else case	
		if distance_less_0 in current_trace_line: #verified
			current_distance_less_0_bool = True
			
		if j_minus_1 in current_trace_line: #buggy?
			current_distance = current_distance + 1
			
		if for_loop_pw_length_check in current_trace_line:
			temp = ord(password_attempt[current_index]) + current_distance
			if current_distance > 0:
				if current_distance_less_0_bool: #then +26 was done
					temp2 = 97 + ((temp - 97) % 26)
					password_reconstructed = password_reconstructed + chr(temp2)
				else: #+26 was not done
					password_reconstructed = password_reconstructed + chr(temp)
								
			current_distance = 0
			current_distance_less_0_bool = False
		
		if return0 in current_trace_line: #verified
			status = 0
			earlier_termination = True
		
		if return1 in current_trace_line: #verified
			status = 1
			if (password_length != password_attempt_length):
				status = 0
			earlier_termination = True
		
		if earlier_termination: #verified
			return (password_reconstructed, status)
			break
		
	print(20 * "*")
	print("STATS")
	print("password_attempt: ", end="")
	print(password_attempt)
	
	print("password_reconstructed: ", end="")
	print(password_reconstructed)
	
	print("password_attempt_length: ", end="")
	print(password_attempt_length)
	
	print("password_length: ", end="")
	print(password_length)
	
	print("current_index: ", end="")
	print(current_index)
	
	print("current_distance_less_0_bool: ", end="")
	print(current_distance_less_0_bool)
	
	print("current_distance: ", end="")
	print(current_distance)
	
	print("status: ", end="")
	print(status)
	print(20 * "*")
		
	return (password_reconstructed, status)

def sub_by_underscore(string, status):		
	for index in range(len(string)):
		if not (ord('a') <= ord(string[index]) and ord(string[index]) <= ord('z')):
			string[index] = "_"
			status = 0
	if status == 0:
		status = "partial"
	else:
		status = "complete"
	return (string, status)

def main():
	task_dir = sys.argv[1]
	task_id = sys.argv[2]
	dir_trace_files = os.listdir(task_dir)
	progress_so_far = ("", 0) #password, check_password output signal
	for trace_file in dir_trace_files:
		with open(os.path.join(task_dir, trace_file), "r") as f:
			trace_lines = f.readlines()
			password_attempt = trace_file[:-4] #remote .txt
			password_reconstructed, status = analyse_trace(trace_lines, password_attempt)
			if len(password_reconstructed) > len(progress_so_far[0]) or status == 1:
				progress_so_far = (password_reconstructed, status)
			#print(progress_so_far)
	
	#print(progress_so_far)
	progress_so_far = sub_by_underscore(progress_so_far[0], progress_so_far[1])
	#print(progress_so_far)
	result = progress_so_far[0] + "," + progress_so_far[1]
#	print(type(task_id))
#	print(task_id)
#	print(len(task_id))
	
	path_of_output = "/home/isl/t2_1/output"
	#path_of_output = "/Users/olivertran/Desktop/ISL6/t2_1/output"
	output_file_name = "oput_" + task_id
	if not os.path.exists(path_of_output):
		os.makedirs(path_of_output)
	with open(os.path.join(path_of_output, output_file_name), "w") as f:
		f.write(result)
		

if __name__ == "__main__":
	main()
