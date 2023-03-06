import telebot
from config import keys, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты цену которой хотите узнать> ' \
           '<имя валюты в которой надо узнать цену первой валюты> <количество переводимой валюты> ' \
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

    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Слишком моного параметров')

        quote, base, amount = values

        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)