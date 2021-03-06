#!/usr/bin/env python3

import collections, functools, math, os.path, sys, traceback


# Represent each potential sum we check as a tuple of an `AxisState` for each axis. This `AxisState`
# represents the index within the input list of integers for the axis, as well as the inclusive
# minimum and maximum indices being considered (to facilitate binary-search per-axis).
AxisState = collections.namedtuple('AxisState', ['index', 'min', 'max'])


class State(tuple):
  """Container for a tuple of AxisState's that does some intelligent hashing."""
  def __hash__(self):
    return hash(tuple(sorted(axis.index for axis in self)))

  def __eq__(self, o):
    return isinstance(o, State) and hash(self) == hash(o)


def get_children(state: State, is_decreasing: bool) -> [State]:
  """Get a list of valid children of the given State tuple.

  is_decreasing determines whether we generate children in a decreasing or increasing direction.
  """
  # Track which indices are used so we can avoid repeated indices in child states.
  used_indices = {axis.index for axis in state}
  children = []
  for idx, axis in enumerate(state):
    # Generate a candidate child for each axis and check for validity.
    if axis.index == axis.min and is_decreasing:
      continue  # There's no lower index to check for this axis.
    if axis.index == axis.max and not is_decreasing:
      continue  # There's no higher index to check for this axis.

    if is_decreasing:
      # Binary-search down on this axis, use current index - 1 as the new (inclusive) max.
      child_min, child_max = axis.min, axis.index - 1
    else:
      # Binary-search up on this axis, use current index + 1 as the new (inclusive) min. 
      child_min, child_max = axis.index + 1, axis.max

    # Pick an index in the center of the valid range, work out from there in case of collisions.
    index = (child_min + child_max) // 2
    # offset, multiplier simply jump back and forth past the midpoint looking for an available
    # index to use.
    offset, multiplier = 1, 1
    while index in used_indices and child_min <= index <= child_max:
      index += offset * multiplier
      offset, multiplier = offset + 1, multiplier * -1

    if not child_min <= index <= child_max:
      continue  # Ran out of indices to try, no valid child to be had here.

    child = AxisState(index, child_min, child_max)

    # Generate a new state tuple, swapping out the child for the right axis.
    children.append(State(state[:idx] + (child,) + state[idx + 1:]))
  return children


def find_sum(input_values: [int], target_sum: int, number_of_axes: int) -> ([State], int):
  """Do a multi-dimensional binary-like-search via breadth-first-search.
  
  Search for `number_of_axes` integers from `input_values` that sum to `target_sum`. Do this by
  breadth-first binary-searching in each axis.

  input_values must be sorted, and number_of_axes must be <= len(input_values)
  """
  # Out of curiosity, track how many summations we try, and how close of a sum we've found.
  total_sums_checked = 0
  closest_sum = None
  closest_state = None

  # Start out roughly centered in the state space by grabbing the middle value for the first index.
  # Note that since valid states may not have duplicate indices, we do some boundary checking to
  # make sure we have enough room for all axes' indices.
  center_index = len(input_values) // 2  # Center-ish, round down.
  start_index = max(center_index - number_of_axes, 0) + number_of_axes - 1

  # Initialize the BFS queue with our starting state. For an input list of 15 integers and 3 axes,
  # for example, our starting state would be:
  #   (AxisState(7, 0, 14), AxisState(6, 0, 13), AxisState(5, 0, 12))
  #
  # In the degenerate case where `number_of_axes` == `len(input_values)` == i.e. 3, you'd get:
  #   (AxisState(2, 0, 2), AxisState(1, 0, 1), AxisState(0, 0, 0))
  #
  # Which can't have any valid children, so just that one state will be checked.
  state_queue = collections.deque([State(
      AxisState(start_index - axis, 0, len(input_values) - axis - 1)
      for axis in range(number_of_axes))])

  # Lots of ways to arrive at the same states, don't revisit the state if we do. Note there's
  # probably some optimization to be done here by memoizing the min/max as well to bound future
  # lookups, but meh. Stores tuples of AxisState directly, because AxisState above ensures we only
  # consider the `index` field for uniqueness checks, regardless of min/max fields.
  checked_states = set()

  try:
    while len(state_queue) > 0:
      current_state = state_queue.popleft()
      # The same state might have been enqueue'd by multiple parents, so check this here as well as
      # when enqueue'ing children later.
      if current_state in checked_states:
        continue
      cur_vals = [input_values[c.index] for c in current_state]
      checked_states.add(current_state)
      current_sum = sum(input_values[axis.index] for axis in current_state)
      total_sums_checked += 1
      if closest_sum is None or abs(current_sum - target_sum) < abs(closest_sum - target_sum):
        closest_sum = current_sum
        closest_state = ', '.join(
          '[%s]=%s' % (axis.index, input_values[axis.index]) for axis in current_state)
      sys.stdout.write('\rClosest sum found: %d, %s, Checked %d summations so far...          ' %
            (closest_sum, closest_state, total_sums_checked))
      if current_sum == target_sum:
        # Hey we found it!
        return total_sums_checked, current_state
      # Keep searching... queue up children we haven't already checked.
      state_queue.extend(filter(lambda child: child not in checked_states,
          get_children(current_state, current_sum > target_sum)))
  
    return total_sums_checked, None # No solution found and we ran out of states to check, time to go home.
  finally:
    print()  # To terminate the status update messages, since they don't print a newline themselves.


def read_input(input_file) -> [int]:
  """Helper to read integers from file, one per line, and sort them. Raises any errors."""
  return sorted([int(line) for line in input_file])


# Print out a handy usage message, in case someone doesn't know how to run me (:
def usage():
  print('Usage: %s target-sum number-of-integers' % os.path.basename(sys.argv[0]))
  print()
  print('  target-sum:  Target sum to search for, probably 2020!')
  print('  number-of-integers:  Number of integers to sum to target-sum')


# Do some basic parsing and use find_sum() above to do the heavy lifting.
def main(argv):
  print('Day 1!')
  print()

  # Too lazy to parseargs, we'll just hand-wave some input checking.
  if len(sys.argv) != 3:
    usage()
    return

  try:
    target_sum = int(sys.argv[1])
    number_of_axes = int(sys.argv[2])
  except ValueError:
    print('Invalid  input, make sure args are integers.')
    print()
    usage()

  try:
    input_values = read_input(sys.stdin)
  except IOError:
    print('IOError reading input from stdin, what did you do?!')
    return
  except ValueError as e:
    print('Invalid input, make sure every line is a single integer!')
    print(e)
    return

  if number_of_axes > len(input_values):
    print("You can't search for %d integers from a list of %d, you doofus >.<" %
          (number_of_axes, len(input_values)))
    return

  print('Searching for %d integers that sum to %d from a list of %d values...' %
        (number_of_axes, target_sum, len(input_values)))

  total_checked, solution = find_sum(input_values, target_sum, number_of_axes)
  print('Checked %s summations, whew that was hard work...' % total_checked)
  if solution is None:
    print('No solution found :( Perhaps you might try bridge.')
  else:
    solution_values = [input_values[axis.index] for axis in solution]
    print('Looks like the numbers %s add up to %s!' % (solution_values, target_sum))
    print('And their product is %d, just in case you were curious...' %
          functools.reduce(lambda a, b: a * b, solution_values))


if __name__ == '__main__':
  main(sys.argv)
