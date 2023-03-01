# функция для сортировки (сортировка пузырьком)
def bubble_sorting(array):
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


# функция для поиска (бинарный поиск)
def binary_search(array, element, left=0, right=None):
    if right is None:
        right = len(array)
        if not array[right - 1] > element > array[left]:  # проверка, если элемент находится за пределами границ списка
            if element < array[left]:
                return f'\nНе возможно установить номер позиции элемента, который меньше введенного числа {element},' \
                       f' а следующий за ним больше или равен числу {element}.\n' \
                       f'Т.к. введеное число {element} меньше минимального числа {array[left]} из заданого списка.'
            else:
                return f'\nНе возможно установить номер позиции элемента, который меньше введенного числа {element},' \
                       f' а следующий за ним больше или равен числу {element}.\n' \
                       f'Т.к. введеное число {element} больше максимального числа {array[right - 1]} из заданого списка.'

    if element in array:  # поиск числа в списке (число точно есть в списке)
        middle = (right + left) // 2

        if array[middle] == element:
            return f'\nРезультат: {array[middle - 1]} - число, которое меньше введеного {element}. Этому числу соответствует индекс {middle - 1} в упорядоченном списке.'
        elif element < array[middle]:
            return binary_search(array, element, left, middle - 1)
        else:
            return binary_search(array, element, middle + 1, right)
    else:  # случай, когда самого числа нет в списке, но оно принадлежит интервалу
        for index, value in enumerate(array):
            if value < element:
                min_value = value
                min_index = index
            else:
                break
        return f'\nРезультат: {min_value} - число, которое меньше введеного {element}. Этому числу соответствует индекс {min_index} в упорядоченном списке.'


try:
    list_num = [int(num) for num in input('Введите список чисел через пробел: ').split()]
    # string_num = '32 5 9 26 4 5 8 10 3 56'
    # string_num = '30 20 10 40 50'
    # list_num = list(map(int, string_num.split()))

    per_value = int(input('Введите любое число: '))
    print(f'Неотсортированный список чисел: {list_num}')

except ValueError:
    print('Введенное значение не является числом')

else:

    sorted_list_num = bubble_sorting(list_num)
    print(f'Отсортированный список чисел: {sorted_list_num}')

    index_per_value = binary_search(list_num, per_value)
    print(index_per_value)
