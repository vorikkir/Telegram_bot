import telebot
import re
import requests
from emoji import emojize
from datetime import datetime
from pprint import pprint


TOKEN = ""
bot = telebot.TeleBot(TOKEN)


euro_type = ['eur', 'euro', 'евро', 'угкщ', 'угк', 'eu', 'e']
usd_type = ['usd', '$', 'гыв', 'баксы', 'доллары','зеленые','баксов','долларов',
            'ye' ,'зеленых', 'дол', 'ue', 'бакс', 'u', 'us']
byn_type = ['byn', 'инт', 'белок', 'бел', 'by', 'ин']
rub_type = ['rub', 'кги', 'россии','рублей', 'ru', 'кг', 'росии', 'рос']

CURRENCY = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
usd = CURRENCY.json()[4]['Cur_OfficialRate']
rub = CURRENCY.json()[16]['Cur_OfficialRate']
euro = CURRENCY.json()[5]['Cur_OfficialRate']
print(usd, euro, rub)


def current_time():
    date = datetime.now()
    date_to_str = datetime.strftime(date, '%d-%m-%Y')
    return date_to_str


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    pprint(message.text)
    try:
        sum_of_money = int(re.search(r'\d*', message.text).group())
        marker = re.search(r'[^\d ]\D*$', message.text).group()
        print(sum_of_money, marker)

        if marker.lower() in usd_type:
            result_byn = str(round((sum_of_money * usd), 2))
            result_euro = str(round((sum_of_money * usd / euro), 2))
            result_ru = str(round((sum_of_money * usd * 100 / rub), 2))
            bot.send_message(message.from_user.id, f'За {sum_of_money} USD Вы получите:\n' + emojize(':Belarus: ') + result_byn +
                         '\n' + emojize(':European_Union: ') + result_euro + '\n' + emojize(':Russia: ') + result_ru)

        elif marker.lower() in euro_type:
            result_byn = str(round((sum_of_money * euro), 2))
            result_usd = str(round((sum_of_money * euro / usd), 2))
            result_ru = str(round((sum_of_money * euro * 100 / rub), 2))
            bot.send_message(message.from_user.id, f'За {sum_of_money} EURO Вы получите:\n' + emojize(':Belarus: ') + result_byn +
                         '\n' + emojize(':United_States: ') + result_usd + '\n' + emojize(':Russia: ') + result_ru)

        elif marker.lower() in rub_type:
            result_byn = str(round((sum_of_money * rub / 100), 2))
            result_usd = str(round((sum_of_money * rub / 100 / usd), 2))
            result_euro = str(round((sum_of_money * rub / 100 / euro), 2))
            bot.send_message(message.from_user.id, f'За {sum_of_money} RUB Вы получите:\n' + emojize(':Belarus: ') + result_byn +
                         '\n' + emojize(':United_States: ') + result_usd + '\n' + emojize(':European_Union: ') + result_euro)

        elif marker.lower() in byn_type:
            result_usd = str(round((sum_of_money / usd), 2))
            result_euro = str(round((sum_of_money / euro), 2))
            result_ru = str(round((sum_of_money * 100 / rub), 2))
            bot.send_message(message.from_user.id, f'За {sum_of_money} BYN Вы получите:\n' + emojize(':United_States: ') + result_usd +
                         '\n' + emojize(':European_Union: ') + result_euro + '\n' + emojize(':Russia: ') + result_ru)

        else:
            time = current_time()
            bot.send_message(message.from_user.id, f'Курсы НБРБ на {time}:\n' + f'usd - {usd}\n' + f'euro - {euro}\n' + f'rub - {rub}\n')
    except:
        bot.send_message(message.from_user.id, "Неправильный формат ввода!\nФормат ввода: 100 usd")

bot.polling()