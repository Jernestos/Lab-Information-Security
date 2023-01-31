import sys
import os
import string

'''
arch     x86
baddr    0x400000
binsz    1007951
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
r2:
0x00401db7 360 main
0x00401db7 360 sym.main
	
0x00401d25 146 sym.check_password
'''

'''
40032:
E:0x4995f0:C:1d2:nop edx, edi 
E:0x4995f4:C:28b:push rbp 
W:0x7fffffffdf30:D
E:0x4995f5:C:176:lea rcx, ptr [rip+0x468c4] 
E:0x4995fc:C:176:lea rdx, ptr [rip+0x468c5] 
E:0x499603:C:19b:mov rbp, rsp 
E:0x499606:C:28b:push r15 
W:0x7fffffffdf28:D
E:0x499608:C:28b:push r14 
W:0x7fffffffdf20:D
E:0x49960a:C:28b:push r13 
W:0x7fffffffdf18:D
E:0x49960c:C:28b:push r12 
W:0x7fffffffdf10:D
E:0x49960e:C:28b:push rbx 
W:0x7fffffffdf08:D
E:0x49960f:C:31b:sub rsp, 0x28 


40057
E:0x49de40:C:1d2:nop edx, edi 
E:0x49de44:C:28b:push rbp 
W:0x7fffffffded0:D
E:0x49de45:C:19b:mov rbp, rsp 
E:0x49de48:C:28b:push r15 
W:0x7fffffffdec8:D
E:0x49de4a:C:19b:mov r15, rdi 
E:0x49de4d:C:28b:push r14 
W:0x7fffffffdec0:D
E:0x49de4f:C:176:lea rax, ptr [rbp-0x38] 
E:0x49de53:C:28b:push r13 
W:0x7fffffffdeb8:D
E:0x49de55:C:28b:push r12 
W:0x7fffffffdeb0:D
E:0x49de57:C:28b:push rbx 
W:0x7fffffffdea8:D
E:0x49de58:C:31b:sub rsp, 0x88 


48086
E:0x410f90:C:1d2:nop edx, edi 
E:0x410f94:C:28b:push rbp 
W:0x7fffffffde70:D
E:0x410f95:C:19b:mov rbp, rsp 
E:0x410f98:C:28b:push r15 
W:0x7fffffffde68:D
E:0x410f9a:C:28b:push r14 
W:0x7fffffffde60:D
E:0x410f9c:C:28b:push r13 
W:0x7fffffffde58:D
E:0x410f9e:C:19b:mov r13d, ecx 
E:0x410fa1:C:28b:push r12 
W:0x7fffffffde50:D
E:0x410fa3:C:19b:mov r12, rdi 
E:0x410fa6:C:28b:push rbx 
W:0x7fffffffde48:D
E:0x410fa7:C:31b:sub rsp, 0x6e8


49685
E:0x401d25:C:1d2:nop edx, edi 
E:0x401d29:C:28b:push rbp 
W:0x7fffffffdf50:D
E:0x401d2a:C:19b:mov rbp, rsp 
E:0x401d2d:C:19b:mov qword ptr [rbp-0x18], rdi 
W:0x7fffffffdf38:D
E:0x401d31:C:19b:mov dword ptr [rbp-0x1c], esi 
W:0x7fffffffdf34:D
E:0x401d34:C:19b:mov qword ptr [rbp-0x28], rdx 
W:0x7fffffffdf28:D
E:0x401d38:C:19b:mov dword ptr [rbp-0x20], ecx 
W:0x7fffffffdf30:D
E:0x401d3b:C:19b:mov eax, dword ptr [rbp-0x1c] 
R:0x7fffffffdf34:D
E:0x401d3e:C:64:cmp dword ptr [rbp-0x20], eax 

'''


#Radare2 output and traces match
'''
47234: main function
E:0x401db7:C:1d2:nop edx, edi 
E:0x401dbb:C:28b:push rbp 
W:0x7fffffffdfd0:D
E:0x401dbc:C:19b:mov rbp, rsp 
E:0x401dbf:C:28b:push r12 
W:0x7fffffffdfc8:D
E:0x401dc1:C:28b:push rbx 
W:0x7fffffffdfc0:D
E:0x401dc2:C:31b:sub rsp, 0x60
...
E:0x401ec9:C:43:call 0x401d25 (call sym.check_password)


49685: check_password function
E:0x401d25:C:1d2:nop edx, edi 
E:0x401d29:C:28b:push rbp 
W:0x7fffffffdf50:D
E:0x401d2a:C:19b:mov rbp, rsp 
E:0x401d2d:C:19b:mov qword ptr [rbp-0x18], rdi 
W:0x7fffffffdf38:D
E:0x401d31:C:19b:mov dword ptr [rbp-0x1c], esi 
W:0x7fffffffdf34:D
E:0x401d34:C:19b:mov qword ptr [rbp-0x28], rdx 
W:0x7fffffffdf28:D
E:0x401d38:C:19b:mov dword ptr [rbp-0x20], ecx 
W:0x7fffffffdf30:D
E:0x401d3b:C:19b:mov eax, dword ptr [rbp-0x1c] 
R:0x7fffffffdf34:D
E:0x401d3e:C:64:cmp dword ptr [rbp-0x20], eax 


check_password(password, strlen(password), argv[1], strlen(argv[1]));

rdi; var_18h -> password
rsi; var_1ch -> strlen(password)
rx; var_28h -> password_attempt
rcx; var_20h -> strlen(password_attempt)

rax: max_length
var_4h -> max_length
var_10h -> pos
var_8h -> k (eq)
var_ch -> j (neq)
'''

#count occurnces when password attempt length is >= strlen(password)
for_loop_pw_length_check = "E:0x401d97" #pos < max_length #occurs strlen(password) + 1 times
inside_for_loop = "E:0x401d5f" #inside for loop, just before the if #occurs strlen(password)
check_for_eq = "E:0x401d81" #if (p[pos] == i[pos]) #occurs strlen(password)
if_branch = "E:0x401d83" #k++ (eq)
else_branch = "E:0x401d89" #j++ (neq)
inc_pos = "E:0x401d8d" #pos++ #occurs strlen(password)

compare_pw_length = "E:0x401d9f" #if (p_size == i_size)
compare_k_with_pw_length = "E:0x401da7" #if (k == p_size)

#note j + k == max_length always

ret_0 = "E:0x401db0" #set ret value to 0
ret_1 = "E:0x401da9" #set ret value to 1

	
def analyse_trace(trace, password_attempt, reconstructed_password):
	max_length = 0
	string_current_index = -1
	
	status = 0
	early_termination = False
	
	for current_trace_line in trace:
		
		if for_loop_pw_length_check in current_trace_line:
			string_current_index = string_current_index + 1
		
		if if_branch in current_trace_line:
			reconstructed_password[string_current_index] = password_attempt[0]
			
		if else_branch in current_trace_line:
			pass
			#reconstructed_password[string_current_index] = password_attempt[0]
		
		if ret_0 in current_trace_line:
			status = 0
			max_length = string_current_index
			early_termination = True
		
		if ret_1 in current_trace_line:
			status = 1
			max_length = string_current_index
			early_termination = True
		
		if early_termination:
			return (max_length, reconstructed_password, status)
			break
	
	print(20 * "*")
	print("STATS")
	print("password_attempt: ", end="")
	print(password_attempt)
		
	print("reconstructed_password: ", end="")
	print(reconstructed_password)
		
	print("max_length: ", end="")
	print(max_length)
		
	print("string_current_index: ", end="")
	print(string_current_index)
				
	print("status: ", end="")
	print(status)
	print(20 * "*")
	
	return (max_length, reconstructed_password, status)
	
	

def sub_by_underscore(string, max_length):
	status = 1		
	for index in range(max_length):
		if not (ord('a') <= ord(string[index]) and ord(string[index]) <= ord('z')):
			string[index] = "_"
			status = 0
	
	if status == 0:
		status = "partial"
	else:
		status = "complete"
	return ("".join(string)[:max_length], status)
	

def main():
	task_id = sys.argv[1]

	#assumptions: password only has small characters [a, z], maximum length is 31 characters
	small_characters = string.ascii_lowercase #not reaccessing it each iteration
	max_password_length = 31
	max_password_length_plus_1 = 32 #in case max password length is 31, for debugging purposes of trace files
	
	Pin = "/home/isl/pin-3.11-97998-g7ecce2dac-gcc-linux-master/"
	SGXTrace = "/home/isl/pin-3.11-97998-g7ecce2dac-gcc-linux-master/source/tools/SGXTrace"
	
	os.chdir(SGXTrace) #do it once
	
	trace_command_1 = "../../../pin -t ./obj-intel64/SGXTrace.so -o "
	trace_command_2 = " -trace 1 -- /home/isl/t2_2/password_checker_2 "
	trace_output_path = "/home/isl/t2_2/"
	trace_file_name = "___trace_file___.txt"
	
	reconstructed_password = list(max_password_length * "_")
	max_length = 0
	status = 0
	
	solution = ""
	
	for password_attempt_character in small_characters:
		#generate password attempt
		#password_attempt = password_attempt_character * max_password_length
		password_attempt = password_attempt_character * max_password_length_plus_1
		
		#follow instructions from handout
#		os.chdir(SGXTrace)
		trace_file_path = trace_output_path + password_attempt_character + trace_file_name
		trace_command = trace_command_1 + trace_file_path + trace_command_2 + password_attempt
		os.system(trace_command)
		
		#read in trace
		with open(trace_file_path, "r") as f:
			trace_lines = f.readlines()
			max_length_, password_reconstructed_, status_ = analyse_trace(trace_lines, password_attempt, reconstructed_password)
			if max_length_ >= max_length:
				password_reconstructed = password_reconstructed_
				status = status_
				max_length = max_length_
				
			solution = "".join(password_reconstructed)[:max_length]
			if "_" not in solution:
				os.remove(trace_file_path)
				break
				
		#remove file
		os.remove(trace_file_path)
	
	
	#print(password_reconstructed)
	#print(status)
	#print(max_length)
	#print(solution)
	status = "complete"
	if "_" in solution:
		status = "partial"
	#(password_reconstructed, status) = sub_by_underscore(password_reconstructed, max_length)
	result = solution + "," + status
	
	path_of_output = "/home/isl/t2_2/output"
#	path_of_output = "/Users/olivertran/Desktop/ISL6/t2_2/output"
	output_file_name = "oput_" + task_id
	if not os.path.exists(path_of_output):
		os.makedirs(path_of_output)
	with open(os.path.join(path_of_output, output_file_name), "w") as f:
		f.write(result)
	
if __name__ == "__main__":
	main()