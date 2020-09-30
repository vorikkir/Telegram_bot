import telebot
import re
import requests
from emoji import emojize
from datetime import datetime



TOKEN = ""
bot = telebot.TeleBot(TOKEN)


euro_type = ['eur', 'euro', 'евро', 'угкщ', 'угк', 'eu', 'e']
usd_type = ['usd', '$', 'гыв', 'баксы', 'доллары','зеленые','баксов','долларов',
            'ye' ,'зеленых', 'дол', 'ue', 'бакс', 'u', 'us']
byn_type = ['byn', 'инт', 'белок', 'бел', 'by', 'ин']
rub_type = ['rub', 'кги', 'россии','рублей', 'ru', 'кг', 'росии', 'рос']


currency = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
usd = currency.json()[4]['Cur_OfficialRate']
rub = currency.json()[16]['Cur_OfficialRate']
euro = currency.json()[5]['Cur_OfficialRate']


def current_time():
    '''Returns the time as a string'''
    date = datetime.now()
    date_to_str = datetime.strftime(date, '%d-%m-%Y')
    return date_to_str

def send_response(id, sum_of_money, result_1, result_2, result_3, marker):
    '''The function sends a response to the user'''
    if marker == 'usd':
        return bot.send_message(id, f'За {sum_of_money} USD Вы получите:\n' + emojize(':Belarus: ') + result_1 +
                         '\n' + emojize(':European_Union: ') + result_2 + '\n' + emojize(':Russia: ') + result_3)
    elif marker == 'euro':
        return bot.send_message(id, f'За {sum_of_money} EURO Вы получите:\n' + emojize(':Belarus: ') + result_1 +
                         '\n' + emojize(':United_States: ') + result_2 + '\n' + emojize(':Russia: ') + result_3)
    elif marker == 'rub':
        return bot.send_message(id, f'За {sum_of_money} RUB Вы получите:\n' + emojize(':Belarus: ') + result_1 +
                         '\n' + emojize(':United_States: ') + result_2 + '\n' + emojize(
                             ':European_Union: ') + result_3)
    elif marker == 'byn':
        return bot.send_message(id, f'За {sum_of_money} BYN Вы получите:\n' + emojize(':United_States: ') + result_2 +
                         '\n' + emojize(':European_Union: ') + result_1 + '\n' + emojize(':Russia: ') + result_3)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    '''The function receives the user's request, converts it, and calls the function send_response'''
    try:
        sum_of_money = float(re.search(r'\d*[^\s|a-z]\d*', message.text).group().replace(',', '.'))
        marker = re.search(r'[^\d ]\D*$', message.text).group()

        if marker.lower() in usd_type:
            result_byn = str(round((sum_of_money * usd), 2))
            result_euro = str(round((sum_of_money * usd / euro), 2))
            result_ru = str(round((sum_of_money * usd * 100 / rub), 2))
            send_response(message.from_user.id, sum_of_money, result_byn, result_euro, result_ru, 'usd')


        elif marker.lower() in euro_type:
            result_byn = str(round((sum_of_money * euro), 2))
            result_usd = str(round((sum_of_money * euro / usd), 2))
            result_ru = str(round((sum_of_money * euro * 100 / rub), 2))
            send_response(message.from_user.id, sum_of_money, result_byn, result_usd, result_ru, 'euro')


        elif marker.lower() in rub_type:
            result_byn = str(round((sum_of_money * rub / 100), 2))
            result_usd = str(round((sum_of_money * rub / 100 / usd), 2))
            result_euro = str(round((sum_of_money * rub / 100 / euro), 2))
            send_response(message.from_user.id, sum_of_money, result_byn, result_usd, result_euro, 'rub')


        elif marker.lower() in byn_type:
            result_usd = str(round((sum_of_money / usd), 2))
            result_euro = str(round((sum_of_money / euro), 2))
            result_ru = str(round((sum_of_money * 100 / rub), 2))
            send_response(message.from_user.id, sum_of_money, result_euro, result_usd, result_ru, 'byn')


        else:
            time = current_time()
            bot.send_message(message.from_user.id, f'Курсы НБРБ на {time}:\n' + f'usd - {usd}\n' + f'euro - {euro}\n' + f'rub - {rub}\n')
    except:
        bot.send_message(message.from_user.id, "Неправильный формат ввода!\nФормат ввода: 100 usd")

bot.polling()

