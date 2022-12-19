set auto-load safe-path
set follow-fork-mode child
set pagination off
set breakpoint pending on

file python3
shell pkill -9 python3

br stringParser
run sp_server.py
br *stringParser+1554
#br *stringParser+1859
c
set var redirectAdmin = 0x7d316c
set var redeemselector = 3
#set var pcVar1 = 1
set var verifyer_second = "0"
c
#c
#p M_response_cleartext
