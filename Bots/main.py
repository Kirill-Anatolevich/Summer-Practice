import time
import telebot
import threading
import re
import requests
from bs4 import BeautifulSoup as BS
import sqlite
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
current_time = 0


def weather_info(message):
    url = 'https://pogoda.mail.ru/prognoz/khimki/'
    page = requests.get(url)
    soup = BS(page.text, 'html.parser')
    weather = soup.find_all('a', class_='information__content__link')
    weather_info_list = []

    for data in weather:
        if data.find('span', class_='weather-icon') is not None:
            weather_info_list.append(data.text)

    weather = weather_info_list[0]

    temperature_pattern = r'[+-]\d+°'
    current_temperature = re.findall(temperature_pattern, weather)
    pressure_pattern = r'\d+\sмм\sрт.\sст.\s\w+\s'
    pressure = re.findall(pressure_pattern, weather)
    humidity_pattern_1 = r'\d+%'
    humidity_pattern_2 = r'влажность\s\w+'
    humidity = re.findall(humidity_pattern_2, weather)[0] + " " + re.findall(humidity_pattern_1, weather)[0]
    wind_pattern_1 = r'\d+\sм/с'
    wind_pattern_2 = r'\w+\sветер'
    wind = re.findall(wind_pattern_2, weather)[0] +" "+ re.findall(wind_pattern_1, weather)[0]
    state_pattern = r'\w+\s+\d+'
    state = re.findall(state_pattern, weather)
    state = re.match(r'\w+', state[0])
    bot.send_message(message.chat.id, f'Температура: {current_temperature[0]}, ощущается как {current_temperature[1]}, '
                              f' {state.group(0)}\n'
                              f'Давление: {pressure[0]}'
                              f'{humidity}\n'
                              f'{wind}')


def Bot():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Bot is ready to work")
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns = ['/weather']
        for btn in btns:
            keyboard.add(telebot.types.KeyboardButton(btn))

        bot.send_message(message.chat.id, 'Список доступных команд', reply_markup=keyboard)

    @bot.message_handler(commands=['weather'])
    def weather(message):
        weather_info(message)

    @bot.message_handler(commands=['help'])
    def get_info(message):
        bot.send_message(message.chat.id, "Для того чтобы установить будильник введите команду: "
                                          "/setalarm [00,23]:[00,59]\n"
                                          "Бот также имеет возможность показывать погоду в текущей момент в Москве"
                                          " командой: /weather")

    @bot.message_handler(content_types=['text'])
    def alarm(message):
        global data_base
        global current_time
        if re.match(r'/setalarm', message.text):
            pattern_time = r"\d+:\d{2}"
            pattern_hour = r"\d+"
            pattern_minute = r":\d{2}"
            time_str = re.search(pattern_time, message.text).group(0)
            hours = re.search(pattern_hour, time_str).group(0)
            minutes = re.search(pattern_minute, time_str).group(0).replace(':', '')
            if int(hours) < 24 and int(minutes) < 60:
                data_base.add_user(message.chat.id, time_str)

        elif message.text == "I wake up!":
            data_base.del_user(message.chat.id, current_time)

        else:
            bot.send_message(message.chat.id, "Не знаю что делать(")

    bot.polling()


def Alarm():
    global data_base
    global current_time
    while True:
        current_time = time.strftime("%H:%M", time.localtime(time.time()))
        for i in range(0, len(data_base.get_time(current_time))):
            bot.send_message(data_base.get_time(current_time)[i][0], "Wake up!")
            # data_base.del_user(data_base.get_time(current_time)[i][0], current_time)
        time.sleep(5)


if __name__ == '__main__':
    data_base = sqlite.SQLiter('base_data.db')
    thread_bot = threading.Thread(target=Bot)
    thread_check = threading.Thread(target=Alarm)
    thread_bot.start()
    thread_check.start()