#!/bin/bash
echo "Start cloning"
rm -rf Information-Security-Lab
git clone https://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@github.com/Jernestos/Information-Security-Lab.git
echo "Cloning terminated"
clear
cd Information-Security-Lab/4/

echo "Sync START"

echo "Sync exe1"
cd exercise1
scp ./exercise1a isl-env:/home/student/handout/exercise1
scp ./exercise1b isl-env:/home/student/handout/exercise1
submit exercise1a ./exercise1a
submit exercise1b ./exercise1b
cd ..
echo "Sync exe1 - DONE"

echo "Sync exe2"
cd exercise2
scp ./exercise2a isl-env:/home/student/handout/exercise2
scp ./exercise2b isl-env:/home/student/handout/exercise2
submit exercise2a ./exercise2a
submit exercise2b ./exercise2b
cd ..
echo "Sync exe2 - DONE"

echo "Sync exe3"
cd exercise3
scp ./exercise3a isl-env:/home/student/handout/exercise3
scp ./exercise3b isl-env:/home/student/handout/exercise3
submit exercise3a ./exercise3a
submit exercise3b ./exercise3b
cd ..
echo "Sync exe3 - DONE"

echo "Sync exe4"
cd exercise4
scp ./exercise4a isl-env:/home/student/handout/exercise4
scp ./exercise4b isl-env:/home/student/handout/exercise4
submit exercise4a ./exercise4a
submit exercise4b ./exercise4b
cd ..
echo "Sync exe4 - DONE"

echo "Sync exe5"
cd exercise5
scp ./exercise5a isl-env:/home/student/handout/exercise5
scp ./exercise5b isl-env:/home/student/handout/exercise5
submit exercise5a ./exercise5a
submit exercise5b ./exercise5b
cd ..
echo "Sync exe5 - DONE"

echo "Sync exe6"
cd exercise6
scp ./exercise6a isl-env:/home/student/handout/exercise6
scp ./exercise6b isl-env:/home/student/handout/exercise6
submit exercise6a ./exercise6a
submit exercise6b ./exercise6b
cd ..
echo "Sync exe6 - DONE"

echo "Sync DONE"

echo "EVAL START"
results
echo "EVAL END"

