per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}

money = int(input('Введите сумму, которую Вы планируете положить на вклад? '))

deposit = list(map(lambda x: int(money * x), per_cent.values()))

print('Максимальная сумма, которую вы можете заработать — %d' % max(deposit))