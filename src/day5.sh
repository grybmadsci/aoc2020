#!/bin/bash -e

TMP=`mktemp`
trap "rm -rf $TMP" EXIT

# Part 1, this problem is just a weird binary encoding where 0's and 1's are F/L and R/B
# respectively. Translate, convert from binary to decimal, then sort | head to find the max.
tr "BFRL" "1010" | (while read BIN; do echo $((2#$BIN)); done) > $TMP
sort -nr $TMP | head -n1


# Similar, but checking the higher-order bits for all-0 or all-1 and checking for presence of the
# seat "id" +/- 1 in the output of Part 1.
seq 1023 | while read SEAT
do
  if grep -qx $SEAT $TMP; then continue; fi
  if test $(($SEAT & 0x3f8)) -eq 0 -o $(($SEAT & 0x3f8)) -eq 1026; then continue; fi
  if grep -qx $((SEAT + 1)) $TMP && grep -qx $((SEAT - 1)) $TMP; then
    echo $SEAT
  fi
done
