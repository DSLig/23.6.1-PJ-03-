import telebot
from config import TOKEN, keys
from utils import ConvExept, Conv

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работать введите команду боту в формате:\n<имя валюты> <в какую валюту перевести> <кол-тво волюты>\nПример:\nдоллар рубль 60\nдоллар рубль\nПользоватьель может увидить все доступные валюты:\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
                    raise ConvExept('Слишком много парамметров.') 
        try:
            base, quote, amount = values
        except ValueError:
            base, quote, = values
            amount = 1
        summ = Conv.convert(base, quote, amount)
    
    except ConvExept as e:
        bot.reply_to(message, f'Ошибка плдьзователя\n{e}')
    
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    
    else:   
        if amount == 1:
            ito = f'Цена {base} за {quote} - {round(summ,2)}'
        else:
            ito = f'Цена {amount} {base} в {quote} - {round(summ,2)}'
        bot.send_message(message.chat.id, ito)

bot.polling()