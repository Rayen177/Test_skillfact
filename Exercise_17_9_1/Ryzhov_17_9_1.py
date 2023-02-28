def sorted_list(array):
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return array


def binary_search(array, element, left=0, right=None):
    if right is None:
        right = len(array)
        if not array[right-1] > element > array[left]:
            if element < array[left]:
                return f'Не возможно установить номер позиции элемента, который меньше введенного числа {element}, а следующий за ним больше или равен числу {element}.\nТ.к. введеное число {element} меньше минимального числа {array[left]} из заданого списка.'
            else:
                return f'Не возможно установить номер позиции элемента, который меньше введенного числа {element}, а следующий за ним больше или равен числу {element}.\nТ.к. введеное число {element} больше максимального числа {array[right-1]} из заданого списка.'

    if element in array:
        middle = (right + left) // 2
        if array[middle] == element:
            return middle - 1
        elif element < array[middle]:
            return binary_search(array, element, left, middle - 1)
        else:
            return binary_search(array, element, middle + 1, right)
    else:
        for i in array:


try:
    # list_num = [int(num) for num in input('Введите список чисел через пробел: ').split()]
    string_num = '32 5 9 26 4 5 8 10 3 56'
    list_num = list(map(int, string_num.split()))
    print(f'Неотсортированный список чисел: {list_num}')
    per_value = int(input('Введите любое число: '))
except ValueError:
    print('Введенное значение не является числом')

else:


    sorted_list_num = sorted_list(list_num)
    print(f'Отсортированный список чисел: {sorted_list_num}')

    index_per_value = binary_search(list_num, per_value)
    print(index_per_value)




