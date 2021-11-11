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
            # Сheck point data
            if isinstance(map[j // map_widht][j % map_widht], int) and isinstance(
                map[i // map_widht][i % map_widht], int
            ):
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
                elif (
                    abs(i // map_widht - j // map_widht) == 1
                    and abs(i % map_widht - j % map_widht) == 1
                ):
                    distances[i][j] = distances[j][i] = (
                        abs(
                            map[i // map_widht][i % map_widht]
                            - map[j // map_widht][j % map_widht]
                        )
                        + 1.5
                    )

    # Dijkstra's algorithm:
    while min(temp_calculated_ways) < shortest_ways_start_to_x[all_points - 1]:
        i = temp_calculated_ways.index(min(temp_calculated_ways))
        temp_calculated_ways[i] = 2000000
        for j in range(all_points):
            try:
                if (
                    distances[i][j] > 0
                    and shortest_ways_start_to_x[j]
                    > shortest_ways_start_to_x[i] + distances[i][j]
                ):
                    shortest_ways_start_to_x[j] = temp_calculated_ways[j] = (
                        shortest_ways_start_to_x[i] + distances[i][j]
                    )
                    parents_points[j] = i
            except TypeError:
                None
    # Get final path from parents point matrix
    i = all_points - 1
    final_best_way.append([i // map_widht, i % map_widht])
    while i > 0:
        final_best_way.append(
            [parents_points[i] // map_widht, parents_points[i] % map_widht]
        )
        i = parents_points[i]

    final_best_way = final_best_way[::-1]
    return (final_best_way, shortest_ways_start_to_x[all_points - 1])


# Check file data
try:
    with open(config["DEFAULT"]["MapPath"], "r", encoding="utf-8") as f:
        map = json.load(f)["map1"]
    # Start point check
    if map[0][0] == "X":
        print("Error: bad start point")
    # End point check
    elif map[-1][-1] == "X":
        print("Error: bad finish point")
    else:
        # Map data check
        try:
            for i in range(len(map[0])):
                for j in range(len(map)):
                    if map[i][j] != "X":
                        try:
                            map[i][j] = int(map[i][j])
                        except ValueError:
                            print(
                                "Warning: Wrong map data in point ["
                                + str(i)
                                + ", "
                                + str(j)
                                + "]"
                            )
            try:
                results = rover(map)
                # Check: if the finish point is not reached, then there is
                # an impassable section on the way

                if results[0][0] == [0, 0] and results[0][-1] == [
                    len(map[0]) - 1,
                    len(map) - 1,
                ]:
                    print(results[0])
                    print("steps: " + str(len(results[0]) - 1))
                    print("fuel: " + str(int(results[1])))
                else:
                    print("Error: Deadend on the way")

            except:
                print("Error: Calculation error")
        except:
            print("Error: bad map size")

except:
    print("Error: Wrong map data")


print("--- %s seconds ---" % (time.time() - start_time))
