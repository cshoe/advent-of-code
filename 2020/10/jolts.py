import sys

lines = [int(l.rstrip('\n')) for l in sys.stdin]
sortedLines = sorted(lines)
sortedLines.insert(0, 0)  # insert 0 for the outlet
sortedLines.append(sortedLines[-1]+3)

visited = [False] * len(lines)
cache = {}


def part1():
    diff_3 = 1  # starts at 1 for the device input
    diff_1 = 0
    for i, joltage in enumerate(sortedLines):
        try:
            diff = sortedLines[i+1] - joltage
        except IndexError:
            break
        else:
            if diff == 3:
                diff_3 += 1
            elif diff == 1:
                diff_1 += 1
    return diff_3 * diff_1


def _build_graph():
    graph = {}

    for i, joltage in enumerate(sortedLines):
        neighbors = []
        for j, test_joltage in enumerate(sortedLines[i+1:i+4]):
            if test_joltage - joltage <= 3:
                neighbors.append(test_joltage)
        graph[joltage] = [neighbors, False]

    return graph


def _find_paths(src, dest, graph, path):
    if src in cache:
        return cache[src]
    path.append(src)
    graph[src][1] = True # mark visited
    local_paths = 0
    if src == dest:
        local_paths += 1
    else:
        for i in graph[src][0]:
            if graph[i][1] is False:
                local_paths += _find_paths(i, dest, graph, path)
    graph[src][1] = False
    cache[src] = local_paths
    return local_paths


def part2():
    graph = _build_graph()
    return _find_paths(0, sortedLines[-1], graph, [])


if __name__ == '__main__':
    print(part1())
    print(part2())
