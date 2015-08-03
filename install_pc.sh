#!/usr/bin/env bash

set -o verbose


echo '##########################################'
echo '# MUST BE RUN IN PATHCRAWLER DIRCTORY!!'
echo '##########################################'

cp ./fcpathcrawler /usr/local/bin
#cp <your path to eclipse>/eclipse PathCrawler/bin
#cp /home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse/lib/i386_linux/* ./bin
cp /home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse_64/eclipse_basic/lib/x86_64_linux/* ./bin
mv ./bin/eclipse.exe ./bin/eclipse
mkdir /usr/local/share/frama-c/pc
cp -r ./bin /usr/local/share/frama-c/pc
cp -r ./lib /usr/local/share/frama-c/pc
cp -r ./share/xml /usr/local/share/frama-c/pc


# original script...
# cp PathCrawler/fcpathcrawler /usr/local/bin
# #cp <your path to eclipse>/eclipse PathCrawler/bin
# cp /home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse/lib/i386_linux/* ./PathCrawler/bin
# mv ./PathCrawler/bin/eclipse.exe ./PathCrawler/bin/eclipse
# mkdir /usr/local/share/frama-c/pc
# cp -r PathCrawler/bin /usr/local/share/frama-c/pc
# cp -r PathCrawler/lib /usr/local/share/frama-c/pc
# cp -r PathCrawler/share/xml /usr/local/share/frama-c/pc
