import subprocess

subprocess.Popen(
"""
echo "KILL PROCESSES 1"
pkill -9 node
pkill -9 string_parser
pkill -9 gdb
#lsof -P -i -n | grep LISTEN
pwd
cd /home/isl/t1
pwd
sleep 3
echo "EXPLOIT 1.1"
screen -Sdm exploit_11 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *0x7ffff74a81d2" -ex "r sp_server.py" -ex "c" -ex 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"' -ex "c" -ex "q"
echo "EXPLOIT 1.1 - END"

sleep 10
echo "KILL PROCESSES 2"
pkill -9 node
pkill -9 string_parser
pkill -9 gdb

sleep 3
echo "EXPLOIT 1.2 - START"
screen -Sdm exploit_12 gdb -batch -ex "set pagination off" -ex "set breakpoint pending on" -ex "set follow-fork-mode child" -ex "set auto-load safe-path" -ex "b stringParser" -ex "b *stringParser+1554" -ex "r sp_server.py" -ex "c" -ex "set var redirectAdmin = 0x7d316c" -ex 'set var verifyer_second = "A"' -ex "set var redeemselector = 3" -ex "c" -ex "q"
echo "EXPLOIT 1.2 - END"
sleep 10
echo "KILL PROCESSES 3"
pkill -9 node
pkill -9 string_parser
pkill -9 gdb
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
