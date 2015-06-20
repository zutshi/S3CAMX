#!/usr/bin/env bash
set -v

for f in ./*.smt2
do
  sed -i 's/(declare-fun dummy_nextstate_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/;(declare-fun dummy_nextstate_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/g' $f
  sed -i 's/(declare-fun dummy_output_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/;(declare-fun dummy_output_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/g' $f
  sed -i 's/(declare-fun state_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/;(declare-fun state_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/g' $f
  sed -i 's/(declare-fun x_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/;(declare-fun x_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/g' $f
  sed -i 's/(declare-fun input_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/;(declare-fun input_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )/g' $f
  sed -i 's/(check-sat)/;(check-sat)/g' $f
  sed -i 's/(exit)/;(exit)/g' $f
done
