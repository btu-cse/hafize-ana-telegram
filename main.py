import telegram.ext
import datetime
from telegram.ext import CallbackContext
from model import Models
import pytz
import requests
import getmenu
import getpdf
import os
import time

yearr = datetime.datetime.now().year
monthh = datetime.datetime.now().month
if monthh == 12:
  monthh = 1
  yearr += 1
else:
  monthh += 1

try:
  newList4, date = getmenu.Menu().get_menu()
except:
  getpdf.GetPdf().get_pdf()
  getpdf.GetPdf().convert_pdf()
  newList4, date = getmenu.Menu().get_menu()

t = True
Token = "TOKEN"

models = Models()
models.create_table()

updater = telegram.ext.Updater(
  "TOKEN", use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


def restart_every_month(context: CallbackContext):
  os.system("rm yemekhane.csv")
  time.sleep(60)
  os.system("kill 1")


j.run_monthly(restart_every_month,
              datetime.datetime(yearr,
                                monthh,
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
    number = datetime.datetime.now().day
  else:
    number = context.args[0]
  if (int(number) > 0):
    bn = (date[int(number) - 1] + " Tarihli Günün Menüsü")
    bnm = newList4[int(number) - 1]
    obnm = bn + "\n" + bnm
    update.message.reply_text(obnm)
  #add message to database
  info = update.message
  messages_to_add(info)


def morning(context: CallbackContext):
  kisilistesi = models.check_all()
  kisisayisi = len(kisilistesi)
  i = 0
  number = datetime.datetime.now().day
  bn = (date[int(number) - 1] + " Tarihli Günün Menüsü")
  bnm = newList4[int(number) - 1]
  obnm = bn + "\n" + bnm

  for i in range(kisisayisi):
    id = kisilistesi[i][0]
    try:
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={id}&text={obnm}"
      requests.get(url).json()
      i += 1
    except:
      print(f"{id} abone olmus ama yetki vermemis")
      i += 1


j.run_daily(morning,
            datetime.time(hour=9,
                          minute=0,
                          tzinfo=pytz.timezone('Europe/Istanbul')),
            days=(0, 1, 2, 3, 4, 5, 6))


def abonelik(update, context):
  user = update.message.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  id = user["id"]
  check_id = models.check_person(id)
  if check_id is None:
    models.add_user(id, first_name, last_name)
    text = "Abonelik kaydınız oluşturuldu! Her gün Saat 09:00'da günün menüsü sizinle paylaşılacaktır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={id}&text={text}"
    requests.get(url).json()
  else:
    text = "Zaten aboneliğiniz bulunmaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={id}&text={text}"
    requests.get(url).json()
  info = update.message
  messages_to_add(info)


def abonelikiptal(update, context):
  user = update.message.from_user
  id = user["id"]
  check_id = models.check_person(id)
  print(check_id)
  if check_id is None:
    text = "Aboneliğiniz bulunmamaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={id}&text={text}"
    requests.get(url).json()
  else:
    models.delete_person(id)
    text = "Aboneliğiniz iptal edilmiştir."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={id}&text={text}"
    requests.get(url).json()
  info = update.message
  messages_to_add(info)


def messages_to_add(info):
  user = info.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  id = user["id"]
  message = info.text
  models.add_message(id, first_name, last_name, message)


dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('menu', getmenu))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('abonelik', abonelik))
dispatcher.add_handler(
  telegram.ext.CommandHandler('abonelikiptal', abonelikiptal))

updater.start_polling()
updater.idle()
