#!/bin/bash -e

# Part 1, this problem is just a weird binary encoding where 0's and 1's are F/L and R/B
# respectively. Translate, convert from binary to decimal, then sort | head to find the max.
tr "BFRL" "1010" | (while read BIN; do echo $((2#$BIN)); done) | sort -nr | head -n1


