#!/bin/bash

echo "### SCRIPT Pre-TEST Start"
echo "This is console output example"
export TEST_PRE_VAR=Pre_Env_Var
echo "TEST_PRE_VAR=$TEST_PRE_VAR"
echo "### SCRIPT Pre-TEST End with return code 99"
exit 99
