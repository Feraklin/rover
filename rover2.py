import json
import time

start_time = time.time()


def rover(map):
    mapWidht = len(map[0])  # количество столбцов "карты"
    S = len(map) * mapWidht  # Количество элементов "карты"
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
            # проверка на точки на полезную информацию
            if isinstance(map[j // mapWidht][j % mapWidht], int) and isinstance(map[i // mapWidht][i % mapWidht], int
                                                                                ):
                if (
                    i // mapWidht == j // mapWidht
                    and abs(i % mapWidht - j % mapWidht) == 1
                ) or (
                    abs(i // mapWidht - j // mapWidht) == 1
                    and i % mapWidht == j % mapWidht
                ):
                    distances[i][j] = distances[j][i] = (
                        abs(
                            map[i // mapWidht][i % mapWidht]
                            - map[j // mapWidht][j % mapWidht]
                        )
                        + 1
                    )
                elif (
                    abs(i // mapWidht - j // mapWidht) == 1
                    and abs(i % mapWidht - j % mapWidht) == 1
                ):
                    distances[i][j] = distances[j][i] = (
                        abs(
                            map[i // mapWidht][i % mapWidht]
                            - map[j // mapWidht][j % mapWidht]
                        )
                        + 1.5
                    )

    # Алгоритм Дейкстры:
    # Считаем, пока минимальное значение в матрице для расчета меньше текущего лучшего
    while min(calcWay) < shortWay[S - 1]:
        i = calcWay.index(min(calcWay))
        # Сразу меняем значение на очень большое, нам нужен был только индекс
        calcWay[i] = 2000000
        for j in range(S):
            # добавлено исключение на случай недопустимых значений
            try:
                # Если сосед и если результат "шага" не превысит текущее лучшее значение
                if distances[i][j] > 0 and shortWay[j] > shortWay[i] + distances[i][j]:
                    # Записываем результаты шага и точку, из которой пришли
                    shortWay[j] = calcWay[j] = shortWay[i] + distances[i][j]
                    parents[j] = i
            except:
                None
    # Воспроизводим путь от финальной точки в первоначальную и "разворачиваем"
    # его
    i = S - 1
    bestWay.append([i // mapWidht, i % mapWidht])
    while i > 0:
        bestWay.append([parents[i] // mapWidht, parents[i] % mapWidht])
        i = parents[i]

    bestWay = bestWay[::-1]
    return (bestWay, shortWay[S - 1])


# Проверка, что есть файл, а в нем что-то лежит
try:
    with open(r"d:\Programming\1\PodgyzBot\rover\map.json", "r", encoding="utf-8") as f:
        map = json.load(f)["map1"]
    # Проверка стартовой точки
    if map[0][0] == "X":
        print("Error: bad start point")
    # Проверка финишной точки
    elif map[-1][-1] == "X":
        print("Error: bad finish point")
    else:
        # Проверка значений на карте переводом в инт
        try:
            for i in range(len(map[0])):
                for j in range(len(map)):
                    if map[i][j] != "X":
                        try:
                            map[i][j] = int(map[i][j])
                        except:
                            print(
                                "Warning: Wrong map data in point ["
                                + str(i)
                                + ", "
                                + str(j)
                                + "]"
                            )
            try:
                results = rover(map)
                # Проверка: если начальная и конечная точка пути не
                # соответствуют заданным, то по пути оказался тупик

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
