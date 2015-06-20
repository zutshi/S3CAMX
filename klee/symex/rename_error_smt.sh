#!/usr/bin/env bash
#set -v
set -e

# for f in ./*.err
# do
  # filename=$(basename "$f")
  # extension="${filename##*.}"
  # filename="${filename%.*}"
  # echo "$filename - $extension"
# done

err_files=()

for f in ./*.err
do
  filename=$(basename "$f")
  # if grep -Fq 'controller_main_symbolic.c:114' $filename
  if grep -Fq 'ASSERTION FAIL: dummy_output_assert & dummy_state_assert' $filename
  then
    IFS='.'; tokens=($filename)
    err_files+=${tokens[0]}
  fi
done

# check if err_files is empty, and if so, throw an error.
# There must be atleast 1 file which has an assertion failure

if [ ${#err_files[@]} -eq 0 ]; then
  #trap 'no assertion failure found. Expected atleast 1!' ERR
  echo 'FATAL: no assertion failure found. Expected atleast 1'
  echo '======================== Exiting! =========================='
  exit -1
fi

for ef in ${err_files}
do
  echo 'renaming ' $ef.smt2 '->' $ef.smt2.error
  mv $ef.smt2 $ef.smt2.error
done

#if grep -Fq 'controller_main_symbolic.c:114' $f


######## NOTES
## Below are an example of TOKENIZATIONs
## (IFS='.'; for word in $filename; do echo "$word"; done)
## IFS='.'; tokens=( $filename )
## echo ${tokens[*]}
# for f in ${tokens[*]}
# do
#   echo $f
# done
#################################################################
