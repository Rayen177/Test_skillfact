'''Понимаю, что понаписал много и возможно оч наворочено, но хотел обыграть все возможные случаи'''
while True:
    try:
        allTickets = int(input('Какое количество билетов Вы хотите приобрести на мероприятие?(введите число): '))
        if allTickets < 0:
            print('Вводимое число не должно быть отрицательным!')
            print()
            continue
        print()
    except ValueError:
        print('Введенное значение не является числом.\nВведите целое число.')
        print()
        continue

    else:
        total_price = 0

        for i in range(allTickets):
            while True:
                try:
                    how_old = int(input(f'Какой возраст {i+1} посетителя, для которого приобретается билет?: '))
                    if how_old < 0:
                        print('Вводимое число не должно быть отрицательным!')
                        print()
                        continue
                    break
                except ValueError:
                    print('Введенное значение не является числом.\nВведите целое число.')
                    print()
                    continue

            if how_old < 18:
                total_price += 0
            elif 18 <= how_old < 25:
                total_price += 990
            else:
                total_price += 1390

    print()
    print(f'Полная стоимость ваших {allTickets} билетов составляет: {str(total_price * 0.9) if allTickets > 3 else str(float(total_price))} руб.')
    break