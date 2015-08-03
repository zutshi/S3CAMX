#!/usr/bin/env bash
set -v

for f in ./*.smt2
do
  sed -i 's/(declare/;(declare/g' $f
  sed -i 's/(check-sat)/;(check-sat)/g' $f
  sed -i 's/(exit)/;(exit)/g' $f
done
