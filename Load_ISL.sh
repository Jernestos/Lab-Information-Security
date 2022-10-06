#!/bin/bash
echo "Start cloning"
rm -rf Information-Security-Lab
git clone https://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@github.com/Jernestos/Information-Security-Lab.git
chmod 755 ./Information-Security-Lab/Load_ISL.sh
rm Load_ISL.sh
mv ./Information-Security-Lab/Load_ISL.sh ~/Desktop
echo "Cloning terminated"
echo "Start test"
cd $HOME/Desktop/Information-Security-Lab/1/Week\ 3\ Lab\ files/
python3.9 module_1_ECDSA_Cryptanalysis.py
