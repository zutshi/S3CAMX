#!/bin/bash
# check for missing 'raise' before err.Fatal
grep -n '^[ ]*err\.Fatal' *

#check for function signature using default list initialization
grep -n '.=\[\]' *
