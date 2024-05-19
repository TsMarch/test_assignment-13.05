import pandas as pd
import itertools
import time
import os
import datetime


def task1():
    """
     Задание 1 имеется текстовый файл f.csv, по формату похожий на .csv с разделителем |
     lastname|name|patronymic|date_of_birth|id Фамилия1|Имя1|Отчество1 |21.11.1998 |312040348-3048 Фамилия2|Имя2|Отчество2 |11.01.1972 |457865234-3431 ...
     Реализовать сбор уникальных записей
     Случается, что под одинаковым id присутствуют разные данные - собрать такие записи
     """
    df = pd.read_csv('f.csv', sep='|')
    df = df.drop(columns=['Unnamed: 0'])
    # оставим только уникальные значения
    df_unique = df.drop_duplicates()
    # соберем разные данные под одинаковым id
    df_same_id = df.groupby('id').filter(lambda x: len(x) > 1).drop_duplicates(keep="first")
    print("Задание 1")
    print("Изначальный датафрейм\n", df)
    print("Датафрейм с уникальниными значениями\n", df_unique)
    print("Датафрейм с разными данными под одинаковым id\n", df_same_id)


def task2():
    """
     Задание 2
     в наличии список множеств. внутри множества целые числа посчитать:
     1. общее количество чисел
     2. общую сумму чисел
     3. посчитать среднее значение
     4. собрать все числа из множеств в один кортеж
     m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]
     *написать решения в одну строку
     """
    m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]
    print("Задание 2")
    # 1
    length = sum([len(i) for i in m])
    print(f"Пункт 1) {length}")
    # 2
    total = sum(itertools.chain(*m))
    total = sum([i for i in m for i in i])
    print(f"Пункт 2) {total}")
    # 3
    avg = total / length
    print(f"Пункт 3) {avg}")
    # 4
    tup = tuple([i for i in m for i in i])
    print(f"Пункт 4) {tup}")


def task3():
    """
     Задание 3 имеется список списков
     a = [[1,2,3], [4,5,6]]
     сделать список словарей
     b = [{'k1': 1, 'k2': 2, 'k3': 3}, {'k1': 4, 'k2': 5, 'k3': 6}]
     *написать решение в одну строку
     """
    a = [[i for i in range(1, 4)], [i for i in range(4, 7)]]
    print("Задание 3:", [{f'k{i}': i for i in x} for x in a])


def task4():
    """
     Имеется папка с файлами реализовать удаление файлов старше N дней
     """

    path = '' # подставить свой путь и добавить path в переменную files
    if not path:
        print("укажите путь для удаления файлов")
    files = os.listdir(path)

    # собираю список из файлов в папке. отмечу, что по условию необходимо удалять только файлы, соответственно папки не войдут в список
    files = [os.path.join(path, file) for file in files if os.path.isfile(file)]
    print("Задание 4")
    print("Файлы в папке до удаления:", *files, sep='\n')

    days = 24 * 3600  # посчитаем сколько секунд в одном дне
    current_time = time.time()
    n = current_time - days * 30  # вычислим в формате unix эпохи момент во времени по которому будем удалять файлы

    # в цикле итерируемся по списку с нашими файлами, сохраняем путь до файла (для его удаления)
    # сохраняем время создания файла в формате unix эпохи
    # удаляем файл если время его создания меньше чем "n"
    for file in files:
        file_location = os.path.join(os.getcwd(), file)
        file_time = os.stat(file_location).st_mtime
        match file_time < n:
            case True:
                # при удалении файла вывожу помимо его названия также дату его создания для наглядности
                print(f"Файл {file} удален, поскольку был создан {datetime.datetime.fromtimestamp(file_time)}")
                os.remove(file_location)

    # по новой собираю список с файлами в директории дабы убедиться что файлы действительно удалились
    print('Задание 4:', "Файлы в папке после удаления:", *[file for file in files if os.path.isfile(file)], sep='\n')


def task5():
    """
     Задание 5*
     Имеется текстовый файл с набором русских слов(имена существительные, им.падеж) Одна строка файла содержит одно слово.
     Написать программу которая выводит список слов, каждый элемент списка которого - это новое слово, которое состоит из двух сцепленных в одно, которые имеются в текстовом файле.
     Порядок вывода слов НЕ имеет значения Например, текстовый файл содержит слова: ласты, стык, стыковка, баласт, кабала, карась
     Пользователь вводмт первое слово: ласты
     Программа выводит: ластык ластыковка
     Пользователь вводмт первое слово: кабала
     Программа выводит: кабаласты кабаласт
     Пользователь вводмт первое слово: стыковка
     Программа выводит: стыковкабала стыковкарась
     """
    inp_word = input("Введите слово для задания 5 из следующего списка: ласты, стык, стыковка, баласт, кабала, карась ")
    words_lst = []
    print("Задание 5")
    with open('words.txt', 'r', encoding='utf-8') as file:
        for line in file:  # итерируемся по словам в файле
            word = line.rstrip()
            step = 1  # создаем шаг для двухстороннего слайсинга
            if word == inp_word:  # если слово пользователя и слово из файла равны - скипаем
                continue
            while step < len(word):  # суть алгоритма в поиске одинаковых символов у слов для сцепки
                inp_word_slice = inp_word[-step:]  # у введенного слова отрезаем с последнего символа
                word_slice = word[:step]  # у итерируемого слова из файла отрезаем с первого символа
                match inp_word_slice == word_slice:  # сравниваем отрезанные символы
                    case True:  # если символы одинаковые то печатаем наше слово и добавляем к нему отрезок оставшихся символов из файла
                        print(f"{inp_word}{word[step:]}")
                        words_lst.append(f"{inp_word}{word[step:]}")
                        break  # выходим из внутреннего цикла while и переходим к следующему слову
                    case False:  # прибавляем шаг если символы не равны
                        step += 1


if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
