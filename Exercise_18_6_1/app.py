import telebot
import requests
import json

TOKEN = '5927698477:AAFRhMDNtAFqBH6S13GcCEcsb5RpTl7qcH8'

bot = telebot.TeleBot(TOKEN)
# @bot.message_handler()
# def func(message):
#     bot.send_message(message.chat.id, f'Hello dear {message.chat.username}')

keys = {'биткоин': 'BTC', 'эфириум': 'ETH', 'доллар':'USD'}
class ConversionException(Exception):
    pass
@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты> ' \
           '\n Увидеть список всех доступных валют - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    values = message.text.split(' ')
    if len(values) > 3:
        raise ConversionException('Слишком моного параметров')
    quote, base, amount = values
    if quote == base:
        raise ConversionException(f'Невозможно перевести одинаковые валюты {base}')
    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConversionException(f'Не удалось обработать валюту {quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConversionException(f'Не удалось обработать валюту {base}')

    try:
        amount = float(amount)
    except ValueError:
        raise ConversionException(f'Не удалось обработать количество {amount}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]

    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)