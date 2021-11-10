import json
import time

start_time = time.time()


def rover(map):
    map_widht = len(map[0])
    all_points = len(map) * map_widht
    bestWay = []  # Кратчайший путь
    shortWay = [100000] * all_points  # Матрица для хранения коротких путей
    shortWay[0] = 0
    calcWay = [100000] * all_points  # Матрица для расчетов коротких путей
    calcWay[0] = 0
    parents = [-1] * all_points  # Матрица для хранения точек пути
    # Матрица для расчета расстояния между соседними точками
    distances = [0] * all_points
    for i in range(all_points):
        distances[i] = [0] * all_points

    # Заполняем матрицу расстояний между соседними точками
    for i in range(all_points):
        for j in range(i + 1, all_points):
            if (
                i // map_widht == j // map_widht and abs(i %
                                                         map_widht - j % map_widht) == 1
            ) or (
                abs(i // map_widht - j //
                    map_widht) == 1 and i % map_widht == j % map_widht
            ):
                distances[i][j] = distances[j][i] = (
                    abs(
                        map[i // map_widht][i % map_widht]
                        - map[j // map_widht][j % map_widht]
                    )
                    + 1
                )

    # Алгоритм Дейкстры:
    # Считаем, пока минимальное значение в матрице для расчета меньше текущего лучшего на финише
    while min(calcWay) < shortWay[all_points - 1]:
        i = calcWay.index(min(calcWay))
        # Сразу меняем значение на очень большое, нам нужен был только индекс
        calcWay[i] = 2000000
        for j in range(all_points):
            # Если сосед и если результат "шага" не превысит текущее лучшее значение
            if distances[i][j] > 0 and shortWay[j] > shortWay[i] + distances[i][j]:
                # Записываем результаты шага и точку, из которой пришли
                shortWay[j] = calcWay[j] = shortWay[i] + distances[i][j]
                parents[j] = i

    # Воспроизводим путь от финальной точки в первоначальную и "разворачиваем" его
    i = all_points - 1
    bestWay.append([i // map_widht, i % map_widht])
    while i > 0:
        bestWay.append([parents[i] // map_widht, parents[i] % map_widht])
        i = parents[i]

    bestWay = bestWay[::-1]
    return (len(bestWay) - 1, shortWay[all_points - 1], bestWay)


with open(r"D:\Программирование\1\PodgyzBot\rover\map.json", "r", encoding="utf-8") as f:
    map = json.load(f)["map1"]

results = rover(map)

print(results[2])
print("steps: " + str(results[0]))
print("fuel: " + str(results[1]))
print("--- %s seconds ---" % (time.time() - start_time))
