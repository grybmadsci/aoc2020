# AoC 2020

Code solutions to [Advent of Code 2020](https://adventofcode.com/2020) puzzle challenge.

Solutions will focus on the spirit of the question, and will include brief descriptions of the
approach used and why.

## Day 1

#### Find 2 integers summing to 2020 from an input list, then find 3 such integers.

### [The Code](src/day1.py)

The obvious linear search solution would be easiest, but cheating a bit and seeing Part 2, the
spirit of this puzzle appears to be around finding a target sum of `M` integers taken from a
collection of `N` integers. This renders the naive linear search method rather inefficient at
<code>O( N<sup>M - 1</sup> )</code>. Leveraging the commutative property of addition, we can cut
down the search space, since there are `M!` duplicate ways to obtain each sum. This might look
familiar from combinatorics, as we end up with a search space of <code>O( <sub>N</sub>C<sub>M</sub>
)</code>. 

Consider that we might be able to do better than a linear search if the input were sorted, which we
can do for an upfront cost of `O( N * log(N) )`, since all axes are the same. This won't affect
overall runtime for `M > 2`. The new search space, then, is in an `M`-dimensional volume with a
monotonic gradient on all axes. This property allows for a forking binary-search style approach,
where each axis must be independently considered. Because of this branching, a tree search algorithm
fits best; I'll go with simple breadth-first search.

I'll represent each `state` as an `M`-tuple of records tracking `index`, `min`, and `max`, where the
index refers to an index in the `N`-integer list (after sorting), and `min` and `max` describe the
range under consideration, a la binary search. As mentioned above, because of the commutative
property of addition, we only need to consider states where each coordinate is strictly less than
the previous. Experimentally, however, the binary search works better with a more open state space,
so in practice, we'll only require that states do not repeat any indices (since we can't
double-count any numbers from the input list). By doing all this, we can get a worst-case runtime
around <code>O( M<sup>log(N)</sup>)</code>, which is way better than a linear search, for some
values of `N`, `M`, and `better`.

### Results

My initial implementation required states to have monotonically decreasing indices in order to
reduce the search space, but the resulting angular shape to the state space made the binary search
not work very well, causing many more states to be checked than seemed right. Instead, I allowed
states to have any indices, so long as there were no duplicates, which performed much better, by a
factor of 4-5 in a couple experiments. States are still treated as duplicates for revisitation
checks if they have the same indices in any order (using custom `__hash__` and `__eq__`
implementations). 

#### Some anecdotal test cases:

> No solution, target sum is too low

```
> seq 100 | ./day1.py 5 5
Day 1!

Searching for 5 integers that sum to 5 from a list of 100 values...
Closest sum found: 15, [1]=2, [0]=1, [4]=5, [3]=4, [2]=3, Checked 12066 summations so far...
Checked 12066 summations, whew that was hard work...
No solution found :( Perhaps you might try bridge.

```

> No solution, target sum is too high

```
> seq 100 | ./day1.py 5 5
Day 1!

Searching for 5 integers that sum to 5 from a list of 100 values...
Closest sum found: 15, [1]=2, [0]=1, [4]=5, [3]=4, [2]=3, Checked 12066 summations so far...
Checked 12066 summations, whew that was hard work...
No solution found :( Perhaps you might try bridge.

```


> No solution, only multiples of 3 can't sum to a non-multiple.


```
> seq 0 3 300 | ./day1.py 100 5
Day 1!

Searching for 5 integers that sum to 100 from a list of 101 values...
Closest sum found: 99, [11]=33, [5]=15, [4]=12, [3]=9, [10]=30, Checked 14289 summations so far...
Checked 14289 summations, whew that was hard work...
No solution found :( Perhaps you might try bridge.

```

Overall this was a fun way to solve this problem. This solution could be generalized to sum values
from different input lists for each axis as well with minor input parsing changes.
