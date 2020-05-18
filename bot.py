
import json
from telegram.ext import CommandHandler,MessageHandler, Filters,Updater
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
import os , sys 
import uploader
from pySmartDL import SmartDL






######################################################################################
bot_token ='811863648:AAGoHSk7JysGIcd1ZchUxP5CcVcQYPaU2DQ'       #

updater = Updater(token=bot_token, use_context=True)                                #

dp = updater.dispatcher                                                          #
                                                                                     #

######################################################################################



def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,text="I am in Beta",parse_mode=telegram.ParseMode.HTML)

@run_async
def start(update,context):
    context.bot.send_message(chat_id =update.message.chat_id,text ="Hey Send me a direct link")

@run_async
def download(update,context):

    url = update.message.text
    url =url.split()
    sent_message =context.bot.send_message(chat_id=update.message.chat_id,text ="Trying To download  ....")

    # dest = "C:\\Downloads\\" # or '~/Downloads/' on linux
    dest = "/app/downloads/"
    # dest = "Downloads\\" #For windows

    try:
        obj = SmartDL(url, dest)
        obj.start()
        
        sent_message.edit_text("Downloading complete")   
        DownloadStatus = True

    except Exception as e :
        print(e)
        sent_message.edit_text("Downloading error :{}".format(e))   
        DownloadStatus = False

    filename = obj.get_dest()
    print(filename)
    # filename = download_file(url)
    try:
        if DownloadStatus:
            sent_message.edit_text("Uploading Your file")   
            wurl = uploader.upload([filename]) 
            sent_message.edit_text(" Full Link : <a href='{}'>Download</a>".format(wurl),parse_mode=ParseMode.HTML)

            try:
              os.remove(filename)
              print("file Removed")
            except Exception as e:
              print(e)
    except Exception as e :
        print(e)
        if DownloadStatus:
            sent_message.edit_text("Uploading fail :".format(e))
            try:
              os.remove(filename)
              print("file Removed")
            except Exception as e:
              print(e)

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

downloader_handler = MessageHandler(Filters.regex(r'http' ), download)
dp.add_handler(downloader_handler)

help_handler = CommandHandler('help',help)
dp.add_handler(help_handler)



updater.start_polling()
updater.idle()
print('Bot Started !')
