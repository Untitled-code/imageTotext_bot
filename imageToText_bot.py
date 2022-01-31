#!/home/investigator/anaconda3/envs/bots_chat/bin/python
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
        bot.sendMessage(chat_id, "Привіт, я бот, допомогти розпізнати текст"
                                 "\n- закінь сюди сканований пдф файл")
        print(msg["text"])
        logging.debug(msg["text"])

    if content_type == 'document':
        file_id = msg['document']['file_id']
        print(file_id)
        logging.debug(file_id)

        # ##### download_file, smaller than one chunk (65K)
        TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        global directory
        directory = f'dir_{chat_id}_{TIMESTAMP}'
        print(f'Directory: {directory}')
        logging.debug(f'Directory: {directory}')
        Path(directory).mkdir(exist_ok=True) #creating a new directory if not exist
        print(f'Directory is made... {directory}')
        logging.debug(f'Directory is made... {directory}')
        inputFile = f'{directory}/input_file_{TIMESTAMP}.pdf'
        print(f'Downloading file to {inputFile}')
        logging.debug(f'Downloading file to {inputFile}')
        bot.download_file(file_id, inputFile)
        bot.sendMessage(chat_id, "Дякую, файл отриманий і опрацьовується... Треба почекати...")
        os.chdir(f'./{directory}') #changing directory to run script
        get_dir = os.getcwd()
        print(f'Working dir is changed to {get_dir}')
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


# replace XXXX.. with your token
TOKEN = "5126764525:AAHuT8ojKuJBQqXpPlOwtzllc2LxmgdyWwI"

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
logging.debug('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
