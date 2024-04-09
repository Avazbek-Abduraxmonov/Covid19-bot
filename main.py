import telebot
import requests
token = 'bot_token'

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(msg):
  cid = msg.chat.id
  markup  = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
  world = telebot.types.KeyboardButton('🌎 World')
  country = telebot.types.KeyboardButton('Country')
  covid_regions = telebot.types.KeyboardButton('Covid Regions')
  markup.add(world)
  markup.add(country, covid_regions)
  bot.send_message(cid, 'Assalomu Aleykum Covid-19 botiga xush kelibsiz!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🌎 World')
def world(msg):
  cid = msg.chat.id

  url = "https://covid-19-tracking.p.rapidapi.com/v1/world"

  headers = {
      "X-RapidAPI-Key": "34fe6d2e50msh7e10501cd13c417p19e723jsnc12607a15468",    "X-RapidAPI-Host": "covid-19-tracking.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers)
  data = response.json().get('Last Update')
  Active = response.json().get('Active Cases_text')
  new = response.json().get('New Cases_text')
  deaths_text = response.json().get('New Deaths_text')
  cases_text = response.json().get('Total Cases_text')
  deaths_text = response.json().get('Total Deaths_text')
  recovered_text = response.json().get('Total Recovered_text')
  bot.send_message(cid, f'World:\n\nLast Update: {data}\nActive: {Active}\nNew: {new}\nNew Deaths: {deaths_text}\nTotal Cases: {cases_text}\nTotal Deaths: {deaths_text}\nTotal Recovered: {recovered_text}')

@bot.message_handler(func=lambda message: message.text == 'Country')
def country(msg):
  cid = msg.chat.id
  country_name = msg.text
  url = "https://covid-19-tracking.p.rapidapi.com/v1/{}".format(country_name)
  headers = {
      "X-RapidAPI-Key": "34fe6d2e50msh7e10501cd13c417p19e723jsnc12607a15468",
      "X-RapidAPI-Host": "covid-19-tracking.p.rapidapi.com"
  }

  try:
      response = requests.get(url, headers=headers)
      if response.status_code == 200:
          name = response.json().get('Country_text')
          data = response.json().get('Last Update')
          Active = response.json().get('Active Cases_text')
          new = response.json().get('New Cases_text')
          deaths_text = response.json().get('New Deaths_text')
          cases_text = response.json().get('Total Cases_text')
          deaths_text = response.json().get('Total Deaths_text')
          recovered_text = response.json().get('Total Recovered_text')

          if 'message' in data:
              bot.send_message(cid, f"Xato: {data['message']}")
          else:
              bot.send_message(cid, f'Nomi: {name}\nSo‘nggi yangilanish: {data}\nAktiv holat: {Active}\nYangi kasalliklar: {new}\nYangi vafotlar: {deaths_text}\nJami kasalliklar: {cases_text}\nJami vafotlar: {deaths_text}\nJami saqlangan: {recovered_text}')
      else:
          bot.send_message(cid, 'Xato: So‘ralgan mamlakat topilmadi')
  except requests.exceptions.HTTPError as e:
      bot.send_message(cid, f"HTTP xatosi ro'y berdi: {e}")
  except requests.exceptions.RequestException as e:
      bot.send_message(cid, f"So‘rovda xato yuz berdi: {e}")


@bot.message_handler(func=lambda message: message.text == 'Covid Regions')
def regions(msg):
    cid = msg.chat.id
    url = "https://covid-19-statistics.p.rapidapi.com/regions"

    headers = {
        "X-RapidAPI-Key": "34fe6d2e50msh7e10501cd13c417p19e723jsnc12607a15468",
        "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json().get('data')

    regions_list = '\n'.join([region.get('name') for region in data])
    bot.send_message(cid, regions_list)


  
print(bot.get_me())
bot.polling()