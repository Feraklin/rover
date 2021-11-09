import json
import time

start_time = time.time()


def rover(map):
    mapWidht = len(map[0])  # количество столбцов "карты"
    S = len(map) * mapWidht  # Количество точек "карты"
    bestWay = []  # Кратчайший путь
    shortWay = [100000] * S  # Матрица для хранения коротких путей
    shortWay[0] = 0
    calcWay = [100000] * S  # Матрица для расчетов коротких путей
    calcWay[0] = 0
    parents = [-1] * S  # Матрица для хранения точек пути
    # Матрица для расчета расстояния между соседними точками
    distances = [0] * S
    for i in range(S):
        distances[i] = [0] * S

    # Заполняем матрицу расстояний между соседними точками
    for i in range(S):
        for j in range(i + 1, S):
            if (
                i // mapWidht == j // mapWidht and abs(i %
                                                       mapWidht - j % mapWidht) == 1
            ) or (
                abs(i // mapWidht - j //
                    mapWidht) == 1 and i % mapWidht == j % mapWidht
            ):
                distances[i][j] = distances[j][i] = (
                    abs(
                        map[i // mapWidht][i % mapWidht]
                        - map[j // mapWidht][j % mapWidht]
                    )
                    + 1
                )

    # Алгоритм Дейкстры:
    # Считаем, пока минимальное значение в матрице для расчета меньше текущего лучшего на финише
    while min(calcWay) < shortWay[S - 1]:
        i = calcWay.index(min(calcWay))
        # Сразу меняем значение на очень большое, нам нужен был только индекс
        calcWay[i] = 2000000
        for j in range(S):
            # Если сосед и если результат "шага" не превысит текущее лучшее значение
            if distances[i][j] > 0 and shortWay[j] > shortWay[i] + distances[i][j]:
                # Записываем результаты шага и точку, из которой пришли
                shortWay[j] = calcWay[j] = shortWay[i] + distances[i][j]
                parents[j] = i

    # Воспроизводим путь от финальной точки в первоначальную и "разворачиваем" его
    i = S - 1
    bestWay.append([i // mapWidht, i % mapWidht])
    while i > 0:
        bestWay.append([parents[i] // mapWidht, parents[i] % mapWidht])
        i = parents[i]

    bestWay = bestWay[::-1]
    return (len(bestWay) - 1, shortWay[S - 1], bestWay)


with open(r"D:\Программирование\1\PodgyzBot\rover\map.json", "r", encoding="utf-8") as f:
    map = json.load(f)["map1"]

results = rover(map)

print(results[2])
print("steps: " + str(results[0]))
print("fuel: " + str(results[1]))
print("--- %s seconds ---" % (time.time() - start_time))
