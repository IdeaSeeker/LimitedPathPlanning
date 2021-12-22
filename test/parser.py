import random


def read_map(path):
    with open(path, 'rt') as map_file:
        lines = list(map(
            lambda line: line.strip(),
            map_file.readlines()
        ))
        height = int(lines[1].split()[1])
        width = int(lines[2].split()[1])
        map_str = '\n'.join([
            ''.join(
                '#' if c != '.' else '.'
                for c in line
            )
            for line in lines[4:]
        ])
        return map_str, width, height


def read_map_scen(path, n_tasks = None):
    tasks = []
    with open(path, 'rt') as map_file:
        lines = list(map(
            lambda line:  line.strip(),
            map_file.readlines()
        ))[1:]
        if not n_tasks is None:
            lines = random.choices(lines, k=n_tasks)
        for line in lines:
            _, _, _, _, start_j, start_i, goal_j, goal_i, result = line.split()
            tasks.append((int(start_i), int(start_j), int(goal_i), int(goal_j), float(result)))
    
    return tasks
