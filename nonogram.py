import itertools, operator

rows = [[7, 3, 1, 1, 7], [1, 1, 2, 2, 1, 1], [1, 3, 1, 3, 1, 1, 3, 1], [1, 3, 1, 1, 6, 1, 3, 1], [1, 3, 1, 5, 2, 1, 3, 1], [1, 1, 2, 1, 1], [7, 1, 1, 1, 1, 1, 7], [3, 3], [1, 2, 3, 1, 1, 3, 1, 1, 2], [1, 1, 3, 2, 1, 1], [4, 1, 4, 2, 1, 2], [1, 1, 1, 1, 1, 4, 1, 3], [2, 1, 1, 1, 2, 5], [3, 2, 2, 6, 3, 1], [1, 9, 1, 1, 2, 1], [2, 1, 2, 2, 3, 1], [3, 1, 1, 1, 1, 5, 1], [1, 2, 2, 5], [7, 1, 2, 1, 1, 1, 3], [1, 1, 2, 1, 2, 2, 1], [1, 3, 1, 4, 5, 1], [1, 3, 1, 3, 10, 2], [1, 3, 1, 1, 6, 6], [1, 1, 2, 1, 1, 2], [7, 2, 1, 2, 5]]

columns = [[7, 2, 1, 1, 7], [1, 1, 2, 2, 1, 1], [1, 3, 1, 3, 1, 3, 1, 3, 1], [1, 3, 1, 1, 5, 1, 3, 1], [1, 3, 1, 1, 4, 1, 3, 1], [1, 1, 1, 2, 1, 1], [7, 1, 1, 1, 1, 1, 7], [1, 1, 3], [2, 1, 2, 1, 8, 2, 1], [2, 2, 1, 2, 1, 1, 1, 2], [1, 7, 3, 2, 1], [1, 2, 3, 1, 1, 1, 1, 1], [4, 1, 1, 2, 6], [3, 3, 1, 1, 1, 3, 1], [1, 2, 5, 2, 2], [2, 2, 1, 1, 1, 1, 1, 2, 1], [1, 3, 3, 2, 1, 8, 1], [6, 2, 1], [7, 1, 4, 1, 1, 3], [1, 1, 1, 1, 4], [1, 3, 1, 3, 7, 1], [1, 3, 1, 1, 1, 2, 1, 1, 4], [1, 3, 1, 4, 3, 3], [1, 1, 2, 2, 2, 6, 1], [7, 1, 3, 2, 1, 1]]

initial = ((3, 3), (3, 4), (3, 12), (3, 13), (3, 21), (8, 6), (8, 7), (8, 10), (8, 14), (8, 15), (8, 18), (16, 6), (16, 11), (16, 16), (16, 20), (21, 3), (21, 4), (21, 9), (21, 10), (21, 15), (21, 20), (21, 21))

grid = [[1 if (i, j) in initial else None for j in range(25)] for i in range(25)]

# Found on StackOverflow somewhere
def combinations_with_replacement_counts(n, r):
  size = n + r - 1
  for indices in itertools.combinations(range(size), n-1):
    starts = [0] + [index+1 for index in indices]
    stops = indices + (size,)
    yield tuple(map(operator.sub, stops, starts))

def cache(lengths):
  retval = []
  for length in lengths:
    dof = 25 - sum(length) - (len(length) - 1)
    boxes = len(length) + 1
    buckets = [[l[0]] + [e + 1 for e in l[1:-1]] + [l[-1]] for l in combinations_with_replacement_counts(boxes, dof)]

    retval.append(list([[e for sublist in [a + b for a, b in zip([[]] + [[1] * r for r in length], [[0] * b for b in bucket])] for e in sublist] for bucket in buckets]))
  return retval

def step(grid, cache):
  for i, row in enumerate(grid):
    product = [1] * 25
    summation = [0] * 25
    cache[i] = [r for r in cache[i] if not any(c is not None and c != l for c, l in zip(row, r))]
    for line in cache[i]:
      product = [a * b for a, b in zip(product, line)]
      summation = [a + b for a, b in zip(summation, line)]
    grid[i] = [1 if b == 1 else a for a, b in zip(grid[i], product)]
    grid[i] = [0 if b == 0 else a for a, b in zip(grid[i], summation)]
  return grid

if __name__ == "__main__":
  # cache all allowable possibilities for each row and column
  # these get filtered at each stage, with possibilities which we have already
  # violated removed
  rowCache = cache(rows)
  columnCache = cache(columns)

  for i in xrange(100):
    step(grid, rowCache)

    grid = map(list, zip(*grid))
    step(grid, columnCache)
    grid = map(list, zip(*grid))

    remaining = sum([g.count(None) for g in grid])

    print "After step", i, "remaining:", remaining

    if remaining == 0:
      print "\n".join(["".join(["x " if e == 1 else "  " for e in g]) for g in grid])
      break
