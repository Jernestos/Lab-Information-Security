import subprocess
import os
import time

os.chdir("/home/isl/t1/")
os.system("kill -9 $(lsof -t -i:3500)")
os.system("kill -9 $(lsof -t -i:4450)")
#os.system("kill -9 $(lsof -t -i:5111)")

command11 = ['gdb', 'batch', '-ex', 'set breakpoint pending on', '-ex', 'set pagination off', '-ex', 'set follow-fork-mode child', '-ex', 'set auto-load safe-path /', '-ex', 'b stringParser', '-ex', 'file python3', '-ex', 'run sp_server.py', '-ex', 'b *(stringParser+1859)', '-ex', 'c', '-ex', 'set M_response_cleartext = "<mes><action type=\\"key-update\\"/></mes>"', '-ex', 'c', '-ex', 'c', '-ex', 'q']

exploit11 = subprocess.Popen(command11, stdin = subprocess.PIPE, text = True)
os.system("sleep 2")
os.system("/home/isl/t1/run_manager.sh")
os.system("/home/isl/t1/run_peripheral.sh")
os.system("/home/isl/t1/start.sh")
os.system("sleep 5")
exploit11.stdin.close()
os.system("kill -9 $(lsof -t -i:5111)")
subprocess.run(['echo "EXPOIT 1.1 TERMINATED"'], shell = True)
os.system("sleep 3")
#subprocess.run(["/home/isl/t1/run.sh"], shell=True)

#
#import subprocess
#import os
#import time
#os.chdir("/home/isl/t1/")
os.system("kill -9 gdb")
os.system("kill -9 $(lsof -t -i:3500)")
os.system("kill -9 $(lsof -t -i:4450)")

command12 = ['gdb', 'batch', '-ex', 'set breakpoint pending on', '-ex', 'set pagination off', '-ex', 'set follow-fork-mode child', '-ex', 'set auto-load safe-path /', '-ex', 'b stringParser', '-ex', 'file python3', '-ex', 'run sp_server.py', '-ex', 'b *(stringParser+1554)', '-ex', 'c', '-ex', 'set var redirectAdmin = 0x7d316c', '-ex', 'set var verifyer_second = 0', '-ex', 'set var redeemselector = 3', '-ex', 'c', '-ex', 'c', '-ex', 'c', '-ex', 'q']
try:
	exploit12 = subprocess.Popen(command12, stdin = subprocess.PIPE, text = True)
	os.system("sleep 2")
	os.system("/home/isl/t1/run_manager.sh")
	os.system("/home/isl/t1/run_peripheral.sh")
	os.system("/home/isl/t1/start.sh")
	os.system("sleep 5")
	exploit12.stdin.flush()
	exploit12.stdin.close()
	subprocess.run(['echo "EXPOIT 1.2 TERMINATED"'], shell = True)
except:
	pass
#os.system("kill -9 $(lsof -t -i:5111)")
subprocess.run(["/home/isl/t1/run.sh"], shell = True)