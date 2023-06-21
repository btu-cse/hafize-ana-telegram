import telegram.ext
import datetime
from telegram.ext import CallbackContext
from model import Models
import pytz
import requests
import getmenu
import scrap
import os
import time

calculatedNextYearDate = datetime.datetime.now().year
calculatedNextMonthDate = datetime.datetime.now().month
if calculatedNextMonthDate == 12:
  calculatedNextMonthDate = 1
  calculatedNextYearDate += 1
else:
  calculatedNextMonthDate += 1

try:
  menuList, date = getmenu.Menu().getFormattedMenu()
except:
  scrap.ScrapMenu().getPdf()
  scrap.ScrapMenu().convertPdfToCsv()
  menuList, date = getmenu.Menu().getFormattedMenu()
Token = "TOKEN"

models = Models()
models.create_table()

updater = telegram.ext.Updater(
  Token, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


def restartEveryMonth(context: CallbackContext):
  os.system("rm yemekhane.csv")
  time.sleep(60)
  os.system("kill 1")


j.run_monthly(restartEveryMonth,
              datetime.datetime(calculatedNextYearDate,
                                calculatedNextMonthDate,
                                1,
                                tzinfo=pytz.timezone('Europe/Istanbul')),
              day=1)


def start(update, context):
  update.message.reply_text(
    "Bursa Teknik Üniversitesi Yemekhane Telegram botuna hoşgeldiniz. /help yazarak komutlara erişebilirsiniz.!"
  )
  info = update.message
  messages_to_add(info)


def help(update, context):
  user = update.message.from_user
  print('You talk with user {} and his user ID: {} and his name is {}'.format(
    user['username'], user['id'], user['first_name']))
  update.message.reply_text("""
    /menu gün -> girdiğiniz günün menüsünü görebilirsiniz, gün girmezseniz içinde olduğunuz günün menüsünü görebilirsiniz.\n\n/abonelik  -> botumuzda abonelik başlatarak her gün saat 09.00'da botumuzdan menüyü telegram'dan özel mesaj olarak alabilirsiniz.(Sadece /abonelik yazarak günlük mesaj alamazsınız botun kendisine tıklayıp mesajlaşma başlatmanız gerekmektedir)\n\n/abonelikiptal -> aboneliğinizi iptal eder.
    """)
  info = update.message
  messages_to_add(info)


def getmenu(update, context):
  if context.args == []:
    userInput = datetime.datetime.now().day
  else:
    userInput = context.args[0]
  if (int(userInput) > 0):
    daysDate = (date[int(userInput) - 1] + " Tarihli Günün Menüsü")
    daysMenu = menuList[int(userInput) - 1]
    daysMenuText = daysDate + "\n" + daysMenu
    update.message.reply_text(daysMenuText)
  #add message to database
  info = update.message
  messages_to_add(info)


def sendDaysMenu(context: CallbackContext):
  kayitliKisiListesi = models.check_all()
  
  
  userInput = datetime.datetime.now().day
  daysDate = (date[int(userInput) - 1] + " Tarihli Günün Menüsü")
  daysMenu = menuList[int(userInput) - 1]
  daysMenuText = daysDate + "\n" + daysMenu

  for eachPerson in range(len(kayitliKisiListesi)):
    telegramId = kayitliKisiListesi[eachPerson][0]
    try:
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={daysMenuText}"
      requests.get(url).json()
      eachPerson += 1
    except:
      print(f"{telegramId} abone olmus ama yetki vermemis")
      eachPerson += 1


j.run_daily(sendDaysMenu,
            datetime.time(hour=9,
                          minute=0,
                          tzinfo=pytz.timezone('Europe/Istanbul')),
            days=("mon", "tue", "wed", "thu", "fri"))


def abonelik(update, context):
  user = update.message.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  telegramId = user["id"]
  check_id = models.check_person(id)
  if check_id is None:
    models.add_user(telegramId, first_name, last_name)
    text = "Abonelik kaydınız oluşturuldu! Her gün Saat 09:00'da günün menüsü sizinle paylaşılacaktır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  else:
    text = "Zaten aboneliğiniz bulunmaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  info = update.message
  messages_to_add(info)


def abonelikiptal(update, context):
  user = update.message.from_user
  telegramId= user["id"]
  check_id = models.check_person(id)
  print(check_id)
  if check_id is None:
    text = "Aboneliğiniz bulunmamaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  else:
    models.delete_person(id)
    text = "Aboneliğiniz iptal edilmiştir."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  info = update.message
  messages_to_add(info)


def messages_to_add(info):
  user = info.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  telegramId = user["id"]
  message = info.text
  models.add_message(telegramId, first_name, last_name, message)


dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('menu', getmenu))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('abonelik', abonelik))
dispatcher.add_handler(
  telegram.ext.CommandHandler('abonelikiptal', abonelikiptal))

updater.start_polling()
updater.idle()
