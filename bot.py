import requests
import telebot
from telebot import types
import ntplib
import pytz 
from datetime import datetime, timedelta
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Токен вашего бота
TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"
bot = telebot.TeleBot(TOKEN)

# Глобальные переменные
ip = '0.0.0.0'  # Начальный IP
is_admin = False
login = 0
cooldowns = {}  # Охлаждение запросов
status_data = {'turn_status': 'неизвестно', 'status': 0}

# Настройки серверов Minecraft
MINECRAFT_SERVERS = {
    'Berkania': '<YOUR_MINECRAFT_SERVER_IP>'
}

# Инициализация файлов
def init_files():
    if not os.path.exists('ip.txt'):
        with open('ip.txt', 'w') as f:
            f.write(ip)
    if not os.path.exists('login.txt'):
        with open('login.txt', 'w') as f:
            f.write("admin")  # Пароль по умолчанию

init_files()

# Загрузка IP
with open('ip.txt', 'r') as f:
    ip = f.read().strip()

# Админ-панель
def admin_panel(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/input_ip')
    btn2 = types.KeyboardButton('/logout')
    btn3 = types.KeyboardButton('/server_status')
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        chat_id,
        "🔧 Админ-панель:\n"
        "/input_ip - Изменить IP сервера\n"
        "/server_status - Проверить статус\n"
        "/logout - Выйти из системы",
        reply_markup=markup
    )

# Обработчики команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    menu = """
🚀 Доступные команды:
/login - Вход в админ-панель
/info - Информация о сервере
/status - Статус сервера
/release - Информация о версии
    """
    bot.reply_to(message, menu)

@bot.message_handler(commands=['login'])
def handle_login(message):
    msg = bot.send_message(message.chat.id, "🔑 Введите админ-пароль:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, check_admin_password)

def check_admin_password(message):
    global is_admin
    try:
        with open('login.txt', 'r') as f:
            correct_password = f.read().strip()
        
        if message.text.strip() == correct_password:
            is_admin = True
            admin_panel(message.chat.id)
        else:
            bot.send_message(message.chat.id, "❌ Неверный пароль!")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {str(e)}")

@bot.message_handler(commands=['logout'])
def handle_logout(message):
    global is_admin
    is_admin = False
    bot.send_message(message.chat.id, "✅ Вы вышли из системы", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['input_ip'])
def handle_input_ip(message):
    if is_admin:
        msg = bot.send_message(message.chat.id, "🌐 Введите новый IP-адрес:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, update_ip_address)
    else:
        bot.reply_to(message, "🔒 Требуется авторизация!")

def update_ip_address(message):
    global ip
    new_ip = message.text.strip()
    try:
        with open('ip.txt', 'w') as f:
            f.write(new_ip)
        ip = new_ip
        bot.reply_to(message, f"✅ IP обновлен: {new_ip}")
        admin_panel(message.chat.id)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

@bot.message_handler(commands=['status', 'server_status'])
def check_status(message):
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{ip}" , verify=False)
        data = response.json()
        status = "🟢 Онлайн" if data['online'] else "🔴 Оффлайн"
        players = f"👥 Игроков: {data['players']['online']}/{data['players']['max']}" if data['online'] else ""
        bot.reply_to(message, f"{status}\n{players}")
        if is_admin:
            admin_panel(message.chat.id)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {str(e)}")

@bot.message_handler(commands=['info'])
def show_info(message):
    """Информация о боте"""
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{ip}" , verify=False)
        data = response.json()
        status = "🟢 Онлайн" if data['online'] else "🔴 Оффлайн"
        players = f"👥 Игроков: {data['players']['online']}/{data['players']['max']}" if data['online'] else ""
        bot.reply_to(message, f"{status}\n{players}")
        if is_admin:
            admin_panel(message.chat.id)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {str(e)}")
    bot.reply_to(message, f"Текущий ip адрес: {ip}\n")

@bot.message_handler(commands=['release'])
def show_version(message):
    """Информация о версии"""
    bot.reply_to(message, "🔖 Версия 4.0\nmade in GANREN™, все права защищены\nЭто последняя версия бота Berkania исходный код доступен на GitHub.")

# Вспомогательные функции
def sync_time():
    """Синхронизация времени с NTP-сервером"""
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        return datetime.fromtimestamp(response.tx_time)
    except Exception as e:
        print(f"Ошибка синхронизации времени: {e}")
        return datetime.now()

def save_data(filename, data):
    """Сохранение данных в файл"""
    with open(f'{filename}.txt', 'w') as f:
        f.write(str(data))

def load_data(filename):
    """Загрузка данных из файла"""
    try:
        with open(f'{filename}.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Инициализация данных
def init_data():
    """Загрузка сохраненных данных"""
    status_data['ip'] = load_data('ip') or '0.0.0.0'
    status_data['status'] = int(load_data('status') or 0)
    status_data['turn_status'] = ['выключен', 'неизвестно', 'включен'][status_data['status'] + 1]

sync_time()
init_data()
print("🤖 Бот успешно запущен!")
bot.infinity_polling()
