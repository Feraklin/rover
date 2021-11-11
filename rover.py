import json
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


start_time = time.time()


def rover(map):
    map_widht = len(map[0])
    all_points = len(map) * map_widht
    final_best_way = []
    shortest_ways_start_to_x = [100000] * all_points
    shortest_ways_start_to_x[0] = 0
    temp_calculated_ways = [100000] * all_points
    temp_calculated_ways[0] = 0
    parents_points = [-1] * all_points
    distances = [0] * all_points
    for i in range(all_points):
        distances[i] = [0] * all_points

    # Fill distances matrix between neighboring points
    for i in range(all_points):
        for j in range(i + 1, all_points):
            if (
                i // map_widht == j // map_widht
                and abs(i % map_widht - j % map_widht) == 1
            ) or (
                abs(i // map_widht - j // map_widht) == 1
                and i % map_widht == j % map_widht
            ):
                distances[i][j] = distances[j][i] = (
                    abs(
                        map[i // map_widht][i % map_widht]
                        - map[j // map_widht][j % map_widht]
                    )
                    + 1
                )

    # Dijkstra's algorithm:
    while min(temp_calculated_ways) < shortest_ways_start_to_x[all_points - 1]:
        i = temp_calculated_ways.index(min(temp_calculated_ways))
        temp_calculated_ways[i] = 2000000
        for j in range(all_points):
            if (
                distances[i][j] > 0
                and shortest_ways_start_to_x[j]
                > shortest_ways_start_to_x[i] + distances[i][j]
            ):
                shortest_ways_start_to_x[j] = temp_calculated_ways[j] = (
                    shortest_ways_start_to_x[i] + distances[i][j]
                )
                parents_points[j] = i

    # Get final path from parents point matrix
    i = all_points - 1
    final_best_way.append([i // map_widht, i % map_widht])
    while i > 0:
        final_best_way.append(
            [parents_points[i] // map_widht, parents_points[i] % map_widht]
        )
        i = parents_points[i]

    final_best_way = final_best_way[::-1]
    return (
        len(final_best_way) - 1,
        shortest_ways_start_to_x[all_points - 1],
        final_best_way,
    )


with open(config["DEFAULT"]["MapPath"], "r", encoding="utf-8") as f:
    map = json.load(f)["map2"]

results = rover(map)

print(results[2])
print("steps: " + str(results[0]))
print("fuel: " + str(results[1]))
print("--- %s seconds ---" % (time.time() - start_time))
