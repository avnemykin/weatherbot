import telebot
import requests
import emoji

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

print(emoji.emojize("Hello, Geek! :thermometer:"))
print(emoji.emojize('Python is :sun:'))
print("\U0001f600")
TOKEN = ''

API_KEY = '68e797c21c4d24f0149e0888beb53eea'

URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'
EMOJI_CODE = {200: u'\U00002601', 800: u"\U00002600", 801: u"\U0001F324", 802: u"\U00002601", 803 : u"\U000026010", 804: u"\U000026010"}


bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard= True)

keyboard.add(KeyboardButton('Получить погоду', request_location=True))

keyboard.add(KeyboardButton('О проекте'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Отправь мне свое местоположение и я отправлю тебе погоду.'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)








def get_weather(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}

    response = requests.get(url=URL_WEATHER_API, params=params).json()
    city_name = response["name"]
    weather = response["weather"][0]
    description = weather["description"]

    main = response["main"]
    code = response["cod"]
    temp = main["temp"]
    temp_feels_like = main["feels_like"]
    humidity = main["humidity"]

    # print(response)
    # print(city_name, description, code, temp, temp_feel_like, humidity)
    emoji_ = EMOJI_CODE[code]
    print(emoji_)
    message = f' Погода в: {city_name}\n'
    message += f'{emoji_} {description.capitalize()}.\n'
    message += f' Температура {temp}°C. \n'
    message += f' Ощущается {temp_feels_like}°C.\n'
    message += f' Влажность {humidity}%.\n'
    return message

@bot.message_handler(content_types=['location'])
def send_weather (message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    if result:
        bot.send_message(message.chat.id, result, reply_markup =keyboard)


bot.infinity_polling()
