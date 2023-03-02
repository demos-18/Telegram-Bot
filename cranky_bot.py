import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConvertor

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом, введите команду в следующем формате: \n<названиние валюты> \
    <в какую валюту преревести> \
    <количество переводимой валюты> \nЧтоб увидеть список доступных валют введите команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        elif len(values) < 3:
            raise APIExeption('Слишком мало параметров.')

        quote, base, amount = values
        total_base = CurrencyConvertor.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()
