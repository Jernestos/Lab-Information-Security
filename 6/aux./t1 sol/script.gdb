set auto-load safe-path
set follow-fork-mode child
set pagination off
set breakpoint pending on

file python3
shell pkill -9 python3

br stringParser
run sp_server.py
br *stringParser+1859
c
set M_response_cleartext = "<mes><action type=\"key-update\"/></mes>" 
p M_response_cleartext
c
