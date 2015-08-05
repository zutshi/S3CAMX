#!/usr/bin/env bash
for f in ./*.py
do
  ## comment
  #sed -i 's/logger\.debug(/# ##!!##logger.debug(/g' $f
  ## uncomment
  sed -i 's/# ##!!##logger\.debug(/logger.debug(/g' $f
done
