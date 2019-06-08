# GetPlaneFromPCL
This is an Entry task for Yandex Self-Driving Meetup 2019. The goal is to find a road plane in the LIDAR Point cloud. It is stated that if more than 50% of PCL points are on or close enough (closer than parameter *p*) to the plane, it's our road plane. That's it. Data is taken from the stdin, and the result is printed to stdout.

**Usage:** `cat input1.txt | ./get_plane.py`

Files input1.txt,input2.txt and input3.txt are the test cases from Yandex (pretty simple ones).

Original task link: [Yandex Self-Driving Meetup 2019 Entry Contest](https://contest.yandex.ru/contest/12698/problems?utm_source=ysdm_mail01)
<details>
<summary>Click here for the original task (Russian language)</summary>
  
### A. Выделить плоскость дороги в лидарном облаке точек
Ограничение времени: 	15 секунд \
Ограничение памяти: 	64Mb \
Ввод 	стандартный ввод или input.txt \
Вывод 	стандартный вывод или output.txt 

#### Задача
Беспилотный автомобиль стоит на ровной асфальтовой площадке, на крыше автомобиля установлен лидар. Даны измерения, полученные лидаром за один период сканирования. 

Измерения представляют собой множество из N точек, имеющих координаты x, y и z. Больше 50% точек принадлежат дороге. Моделью положения принадлежащих дороге точек в пространстве является плоскость с параметризацией *A⋅x+B⋅y+C⋅z+D=0*.

Точки, которые принадлежат дороге, отклоняются от модели не больше чем на заданную величину p.

Необходимо найти параметры A, B, C, и D соответствующей дороге плоскости. Число точек, отклоняющихся от модели не больше чем на p, должно составлять не менее 50% от общего числа точек.

#### Формат ввода
Входные данные заданы в текстовом формате. Первая строка содержит фиксированный порог p (0.01≤p≤0.5). Вторая строка содержит число точек N (3≤N≤25000). Следующие N строк содержат координаты x, y и z (−100≤x,y,z≤100) для каждой точки, разделителем является символ табуляции (формат строки "x[TAB]y[TAB]z"). Вещественные числа имеют не более 6 десятичных знаков.
Формат вывода
Выведите параметры A, B, C, и D соответствующей дороге плоскости. Числа разделяйте пробелами. Выведенные параметры должны задавать корректную плоскость. 
  
</details>

Ths task is solved using a simple RANSAC, and can be speeded up dramatically by parallelization (CUDA, for example). The latter was impossible for this challenge.

## Credits
[Yury D.](https://github.com/OwlSoul) (TheOwlSoul@gmail.com)
