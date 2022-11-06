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
scp ./exploit1a.py isl-env:/home/student/handout/exercise1
scp ./exploit1b.py isl-env:/home/student/handout/exercise1
npx isl-tool@latest submit ex1a ./exploit1a.py
npx isl-tool@latest submit ex1b ./exploit1b.py
cd ..
echo "Sync exe1 - DONE"

echo "Sync exe2"
cd exercise2
scp ./exploit2a.py isl-env:/home/student/handout/exercise2
scp ./exploit2b.py isl-env:/home/student/handout/exercise2
npx isl-tool@latest submit ex2a ./exploit2a.py
npx isl-tool@latest submit ex2b ./exploit2b.py
cd ..
echo "Sync exe2 - DONE"

echo "Sync exe3"
cd exercise3
scp ./exploit3a.py isl-env:/home/student/handout/exercise3
scp ./exploit3b.py isl-env:/home/student/handout/exercise3
npx isl-tool@latest submit ex3a ./exploit3a.py
npx isl-tool@latest submit ex3b ./exploit3b.py
cd ..
echo "Sync exe3 - DONE"

echo "Sync exe4"
cd exercise4
scp ./exploit4a.py isl-env:/home/student/handout/exercise4
scp ./exploit4b.py isl-env:/home/student/handout/exercise4
npx isl-tool@latest submit ex4a ./exploit4a.py
npx isl-tool@latest submit ex4b ./exploit4b.py
cd ..
echo "Sync exe4 - DONE"

echo "Sync exe5"
cd exercise5
scp ./exploit5a.py isl-env:/home/student/handout/exercise5
scp ./exploit5b.py isl-env:/home/student/handout/exercise5
npx isl-tool@latest submit ex5a ./exploit5a.py
npx isl-tool@latest submit ex5b ./exploit5b.py
cd ..
echo "Sync exe5 - DONE"

echo "Sync exe6"
cd exercise6
scp ./exploit6a.py isl-env:/home/student/handout/exercise6
scp ./exploit6b.py isl-env:/home/student/handout/exercise6
npx isl-tool@latest submit ex6a ./exploit6a.py
npx isl-tool@latest submit ex6b ./exploit6b.py
cd ..
echo "Sync exe6 - DONE"

echo "Sync DONE"

echo "EVAL START"
results
echo "EVAL END"

