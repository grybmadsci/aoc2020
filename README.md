# AoC 2020

Code solutions to [Advent of Code 2020](https://adventofcode.com/2020) puzzle challenge.

Solutions will focus on the spirit of the question, and will include brief descriptions of the approach used and why.

## Day 1

#### Find 2 integers summing to 2020 from an input list, then find 3 such integers.

[The Code](src/day1.py)

The obvious linear search solution would be easiest, but cheating a bit and seeing Part 2, the spirit of this puzzle appears to be around finding a target sum of `M` integers taken from a collection of `N` integers. This renders the naive linear search method rather inefficient at <code>O(N<sup>M - 1</sup>)</code>. Leveraging the commutative property of addition, we can cut down the search space, since there are `M!` 'copies' of each sum. This might look familiar from combinatorics, as we end up with a search space of ![O(N choose M)](http://www.sciweavers.org/tex2img.php?eq=O%28%5Cbinom%7BN%7D%7BM%7D%29&bc=Transparent&fc=Black&im=png&fs=12&ff=arev&edit=0).

Consider that we might be able to do better than a linear search if the input were sorted, which we can do for an upfront cost of `O(N * log(N))`, since all axes are the same. This won't affect overall runtime for `M > 2`. The new search space, then, is in an `M`-dimensional volume with a monotonic gradient on all axes. This property allows for a forking binary-search style approach, where each axis must be independently considered. Because of this branching, a tree search algorithm fits best; I'll go with simple breadth-first search.


I'll represent each `state` as an `M`-tuple of records tracking `index`, `min`, and `max`, where the index refers to an index in the `N`-integer list (after sorting), and `min` and `max` describe the range under consideration, a la binary search. As mentioned above, because of the commutative property of addition, we only need to consider states where each coordinate is strictly less than the previous.
