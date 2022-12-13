import telegram.ext
import datetime
from itertools import islice, cycle
from telegram.ext import CallbackContext
from model import Models
import pytz
import requests
import getmenu
import getpdf

try:
  newList4, date = getmenu.Menu().get_menu()
except:
  getpdf.GetPdf().get_pdf()
  getpdf.GetPdf().convert_pdf()
  newList4, date = getmenu.Menu().get_menu()

t = True
Token = "5563013111:AAEqy7baa_AIzWkz-uFtRPi9M8W7vDN9WS0"

models = Models()
models.create_table()



updater = telegram.ext.Updater(
  "5563013111:AAEqy7baa_AIzWkz-uFtRPi9M8W7vDN9WS0", use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


def start(update, context):
  update.message.reply_text(
    "Bursa Teknik Üniversitesi Yemekhane Telegram botuna hoşgeldiniz. /help yazarak komutlara erişebilirsiniz.!"
  )


def help(update, context):
  user = update.message.from_user
  print('You talk with user {} and his user ID: {} and his name is {}'.format(
    user['username'], user['id'], user['first_name']))
  update.message.reply_text("""
    /menu gün -> girdiğiniz günün menüsünü görebilirsiniz, gün girmezseniz içinde olduğunuz günün menüsünü görebilirsiniz.\n\n/abonelik  -> botumuzda abonelik başlatarak her gün saat 09.00'da botumuzdan menüyü telegram'dan özel mesaj olarak alabilirsiniz.(Sadece /abonelik yazarak günlük mesaj alamazsınız botun kendisine tıklayıp mesajlaşma başlatmanız gerekmekte)\n\n/abonelikiptal -> aboneliğinizi iptal eder.
    """)


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
j.run_daily(morning, datetime.time(hour=4, minute=4, tzinfo=pytz.timezone('Europe/Istanbul')), days=(0, 1, 2, 3, 4, 5, 6))

def abonelik(update, context):
  user = update.message.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  id = user["id"]
  check_id = models.check_person(id)
  if check_id is None:
    models.add_user(id, first_name, last_name)
    update.message.reply_text(
      f"Abonelik kaydınız oluşturuldu! Her gün Saat 09:00'da günün menüsü sizinle paylaşılacaktır."
    )
  else:
    update.message.reply_text(f"Zaten aboneliğiniz bulunmaktadır.")


def abonelikiptal(update, context):
  user = update.message.from_user
  id = user["id"]
  check_id = models.check_person(id)
  print(check_id)
  if check_id is None:
    update.message.reply_text(f"Aboneliğiniz bulunmamaktadır.")
  else:
    models.delete_person(id)
    update.message.reply_text(f"Aboneliğiniz iptal edilmiştir.")


dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
#dispatcher.add_handler(telegram.ext.CommandHandler('mesajat', mesajat))
dispatcher.add_handler(telegram.ext.CommandHandler('menu', getmenu))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('abonelik', abonelik))
dispatcher.add_handler(
  telegram.ext.CommandHandler('abonelikiptal', abonelikiptal))

updater.start_polling()
updater.idle()
