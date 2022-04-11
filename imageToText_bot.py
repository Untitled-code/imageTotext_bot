import subprocess
import os
import time
import telepot
from telepot.loop import MessageLoop
from pathlib import Path
import datetime
import glob
import logging

logging.basicConfig(filename='imageToText_bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    logging.debug(content_type, chat_type, chat_id)
    if content_type == 'text':
        bot.sendMessage(chat_id, "Привіт! Допомогти розпізнати текст?"
                                 "\nЗакинь сюди сканований PDF-файл або просто скан документа")
        print(msg["text"])
        logging.debug(msg["text"])

    if content_type == 'document':
        print(msg)
        file_id = msg['document']['file_id']
        print(file_id)
        logging.debug(file_id)
        who_sent = msg['from']['first_name']
        print(f'Doc was sent by...{who_sent}')
        logging.debug(f'Doc was sent by...{who_sent}')
        ext = 'pdf'
        prepareFolder(chat_id, who_sent, file_id, ext)
        subprocess.run('../convertRecognizeScan.sh')
        # let the human know that the file is on its way
        bot.sendMessage(chat_id, "готую файл для відправки ...")
        file = glob.glob(f"text_*.txt")
        print(file) #glob returns file in list format :(
        logging.debug(file) #glob returns file in list format :(
        # send the pdf doc
        bot.sendDocument(chat_id=chat_id, document=open(file[0], 'rb'))

        bot.sendMessage(chat_id, "Тримай!")
        os.chdir(f'{os.environ.get("HOME")}/PycharmProjects/imageTotext_bot')
        get_home_dir = os.getcwd()
        print(f'Working dir is changed to home folder {get_home_dir}')

    if content_type == 'photo':
        file_id = msg['photo'][2]['file_id'] # get photo in the highest res
        print(file_id)
        print(msg)
        logging.debug(file_id)
        who_sent = msg['from']['first_name']
        print(f'Photo was sent by...{who_sent}')
        logging.debug(f'Doc was sent by...{who_sent}')
        ext = 'jpg'
        prepareFolder(chat_id, who_sent, file_id, ext)

        subprocess.run('../scanAndClean.sh')
        # let the human know that the file is on its way
        bot.sendMessage(chat_id, "готую файл для відправки ...")
        file = glob.glob(f"text_*.txt")
        print(file) #glob returns file in list format :(
        logging.debug(file) #glob returns file in list format :(
        # send the pdf doc
        bot.sendDocument(chat_id=chat_id, document=open(file[0], 'rb'))

        bot.sendMessage(chat_id, "Тримай!")
        os.chdir(f'{os.environ.get("HOME")}/PycharmProjects/imageTotext_bot')
        get_home_dir = os.getcwd()
        print(f'Working dir is changed to home folder {get_home_dir}')

def prepareFolder(chat_id, who_sent, file_id, ext):
    # ##### download_file, smaller than one chunk (65K)
    TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    global directory
    directory = f'dir_{chat_id}_{who_sent}_{TIMESTAMP}'
    print(f'Directory: {directory}')
    logging.debug(f'Directory: {directory}')
    Path(directory).mkdir(exist_ok=True)  # creating a new directory if not exist
    print(f'Directory is made... {directory}')
    logging.debug(f'Directory is made... {directory}')
    inputFile = f'{directory}/input_file_{TIMESTAMP}.{ext}'
    print(f'Downloading file to {inputFile}')
    logging.debug(f'Downloading file to {inputFile}')
    bot.download_file(file_id, inputFile)
    bot.sendMessage(chat_id, "Дякую, файл отриманий і опрацьовується... Треба почекати...")
    os.chdir(f'./{directory}')  # changing directory to run script
    get_dir = os.getcwd()
    print(f'Working dir is changed to {get_dir}')

# replace XXXX.. with your token
TOKEN = ""

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
logging.debug('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
