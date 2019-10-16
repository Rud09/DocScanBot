from telegram.ext import Updater , CommandHandler , MessageHandler , Filters
import os
import requests
import logging
from scan import convert,toPdf

def start(update,context):
    context.bot.send_message(chat_id=update.message.chat_id,text="Hello I'm Friday, Nice to meet you!!")

def convert_uppercase(bot,update):
    update.message.reply_text(update.message.text.upper())

def get_url():
    contents=requests.get('https://random.dog/woof.json').json()
    url=contents['url']
    return url

def bop(update,context):
    url=get_url()
    context.bot.send_photo(chat_id=update.message.chat_id,photo=url)

def getPic(update,context):
    pic=context.bot.get_file(update.message.photo[-1].file_id)
    pic.download('test.jpg') 
    doc,flag=convert('test.jpg')
    if flag==0:
        context.bot.send_message(chat_id=update.message.chat_id,text=doc)
    else:
        context.bot.send_photo(chat_id=update.message.chat_id,photo=open(doc,'rb'))
        toPdf(doc)
        context.bot.send_document(chat_id=update.message.chat_id,document=open('doc.pdf','rb'))
        os.remove('doc.jpg')
        os.remove('doc.pdf')
        #print("done")
    os.remove('test.jpg')
    #print("success")

def main():

    updater = Updater(token=os.environ['BOT_TOKEN'],use_context=True)
    dispatcher = updater.dispatcher
    print("Powered ON!!")
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    #add command handler to dispatcher
    start_handler = CommandHandler('start',start)
    #upper_case = MessageHandler(Filters.text,convert_uppercase)
    dispatcher.add_handler(start_handler)
    #dispatcher.add_handler(upper_case)
    bop_handler=CommandHandler('bop',bop)
    dispatcher.add_handler(bop_handler)

    dispatcher.add_handler(MessageHandler(Filters.photo,getPic))

    #starting bot
    updater.start_polling()

    #run bot until ctrl+c is pressed
    updater.idle()

if __name__ == "__main__":
    main()