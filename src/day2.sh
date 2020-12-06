#!/bin/bash -e

# Save a copy of the input for part 2, delete it on exit.
TMP=`mktemp`
trap "rm -rf $TMP" EXIT

# Part 1

# Translate '1-2 x: ---' to a shell command that counts the occurrences of the character 'x' in ---
# and compares it against the counts 1 and 2, printing a dot if the count is valid. Then evaluate
# those shell commands and count the number of dots printed with wc.

echo -n 'Part 1: '
tee $TMP | sed -r '
  s/^([0-9]+)-([0-9]+) (.): (.+)$/T=`echo \4 | tr -dc \3 | wc -c`; test $T -ge \1 -a $T -le \2 \&\& echo .;/
' | source /dev/stdin | wc -l

# Very similar translation, but instead of counting 'x' characters, cut just the characters at
# positions 1 and 2, then count how many 'x' characters there are and print a dot if it's exactly 1.

echo -n 'Part 2: '
sed -r '
  s/^([0-9]+)-([0-9]+) (.): (.+)$/T=`echo \4 | cut -c\1,\2 | tr -dc \3 | wc -c`; test $T -eq 1 \&\& echo .;/
' $TMP | source /dev/stdin | wc -l

