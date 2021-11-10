# rover
Rover. Finding the shortest path by Dijkstra’s shortest path algorithm

## Задача
Вы — инженер, проектирующий роверы-беспилотники. Вам надо спроектировать путь ровера по заранее известной местности с максимальной экономией заряда.

## Местность
Вам пришли данные о местности в закодированном виде: фотография, сконвертированная в матрицу с числами. Одна матрица — это прямоугольный снимок размером х на y метров. Вот пример одной такой сконвертированной фотографии, на ней снимок в 100 на 100 метров:
```sh 
Фото 1: 
0 2 3 4 1
2 3 4 4 1
3 4 5 6 2
4 5 6 7 1
6 7 8 7 1
```

Числа показывают высоту над уровнем моря. 0 — это высота ровно на уровне моря, а, например, 4 — это 4 единицы над уровнем моря. На Фото 1 закодирован холм, пологий слева и резко обрывающийся справа.
Небольшой холмик выглядел бы вот так

```sh 
Фото 2: 
0 1 1 1 0
1 1 3 1 1
0 1 1 1 0
0 0 0 0 0
```

А вот так: ложбина между двумя холмами
```sh 
Фото 3: 
1 1 2 3 4
1 0 1 2 3
2 1 1 1 2
3 3 1 0 1
4 3 1 1 0
```

На этих данных - скала или овраг, так как виден очень резкий перепад высот в середине снимка
```sh 
Фото 4: 
1 1 6 7 7
1 1 6 7 8
1 6 7 8 9
```

А на этом - маленькая ямка 

```sh 
Фото 5: 
3 4 4 4 4 3
3 2 1 1 1 4
4 2 1 1 3 4
4 4 2 2 3 4
```

Данные придут вам в виде матрицы с неотрицательными числами. Размер матрицы NxM.

## Ровер
Ровер всегда движется из верхней левой точки [0][0] в правую нижнюю точку [N - 1][M - 1], где N и M - это длина и ширина матрицы. Это надо для того, чтобы разрезать фотографию на одинаковые куски, обработать их по-отдельности, а потом склеить весь путь.
У вашего ровера есть несколько ограничений:

### Движение
Из любой точки ровер может двигаться только в четыре стороны: на север, юг, запад, восток. Ровер не может ехать по-диагонали — эта функция еще не реализована. Ровер не может вернуться в ту точку, в которой уже был.
### Заряд
Ровер ездит на заряде. Вы знаете, что для ровера очень затратно подниматься и опускаться. Он тратит единицу заряда на само движение, и дополнительные единицы на подъем и спуск. Ровер бы вообще спокойно жил, если бы ездил по асфальту в Беларуси, тогда бы он тратил себе линейно заряд и в ус не дул, но жизнь его сложилась иначе.
### Расход заряда
Заряд расходуется по правилу:
На 1 шаг ровер всегда тратит 1 единицу заряда. На подъем или спуск ровер тратит заряд, пропорциональный сложности подъема или спуска. Сложность подъема или спуска - это разница между высотами. 


Например, в такой местности 
```sh 
1 2
1 5
```
на путь из [0][0] в [0][1] ровер потратит 2 единицы заряд: 1 единица заряда на само движение, и еще 1 единицу заряда на подъем в [0][1]. А из [0][1] в [1][1] ровер потратит 4 единицы заряда: 1 единица на само движение, и 3 единицы (5 - 2) на подъем
Вам надо рассчитать путь ровера из верхей левой [0][0] точки в правую нижнюю [N - 1][M - 1] точку с минимальной тратой заряда.
Вы не заранее знаете размер фотографии, которую будете обрабатывать, N и M - произвольные неотрицательные числа.

## План
Сделайте план пути и планируемый расход и выведите.
Для фотографии
```sh 
0 4
1 3
```
план будет такой:

```sh 
[0][0]->[1][0]->[1][1]
steps: 2
fuel: 5
```
Ровер едет из 0 в 1 в 3, сделает два шага, потратит 5 заряда. Если бы он поехал сначала в 4, потом в 3, он бы сделал то же количество шагов, но потратил бы 7 заряда. Оптимальный путь: 2 шага и 5 заряда.
Если на карте есть несколько вариантов пути, выберите любой из них.
