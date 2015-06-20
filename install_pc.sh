#!/usr/bin/env bash
set -o verbose

cp PathCrawler/fcpathcrawler /usr/local/bin
#cp <your path to eclipse>/eclipse PathCrawler/bin
cp /home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse/lib/i386_linux/* ./PathCrawler/bin
mv ./PathCrawler/bin/eclipse.exe ./PathCrawler/bin/eclipse
mkdir /usr/local/share/frama-c/pc
cp -r PathCrawler/bin /usr/local/share/frama-c/pc
cp -r PathCrawler/lib /usr/local/share/frama-c/pc
cp -r PathCrawler/share/xml /usr/local/share/frama-c/pc

echo 'exporting LD_LIBRARY_PATH and ECLIPSEDIR...'
export LD_LIBRARY_PATH+=:/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse/lib/i386_linux/
export ECLIPSEDIR=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/extras/eclipse/
