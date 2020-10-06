from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

import requests
import re


def get_data(query):
    try:
        city = requests.get(
            'https://www.metaweather.com/api/location/search/?query='+query).json()[0]
        city_title = city['title']
        city_id = city['woeid']

        contents = requests.get(
            'https://www.metaweather.com/api/location/'+str(city_id)).json()
        data = contents['consolidated_weather'][0]
        print(data)

        temepratue = round(float(data['the_temp']), 1)
        min_temp = round(float(data['min_temp']), 1)
        max_temp = round(float(data['max_temp']), 1)
        humidity = round(float(data['humidity']), 1)
        weather_state = data['weather_state_abbr']
        weather_state_name = data['weather_state_name']
        picture = 'https://www.metaweather.com/static/img/weather/png/'+weather_state+'.png'

        final_data = f"Weather for <b>{city_title}</b>\n<a href=\"{picture}\">{weather_state_name}</a>\nTemperature: <b>{temepratue}°C</b> \nMinimum Temperature: <b>{min_temp}°C</b> \nMaximum Temperature: <b>{max_temp}°C</b> \nHumidity: <b>{humidity}</b>"

    except:
        final_data = f"Couldn't find <b>{query}</b>"

    return final_data


def get_weather(bot, update):
    print(update.message.text)
    message = update.message.text
    query = message[message.find(' ')+1:]

    data = get_data(query)
    chat_id = update.message.chat_id

    bot.send_message(
        chat_id=chat_id, text=data, parse_mode=ParseMode.HTML)


def main():
    updater = Updater('TOKEN')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('weather', get_weather))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
