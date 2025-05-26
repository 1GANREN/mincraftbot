RU
Документация для обычного пользователя
Что делает этот бот?

Этот Telegram-бот предназначен для управления и мониторинга состояния сервера Minecraft. Основные возможности включают проверку статуса сервера, изменение IP-адреса сервера и получение информации о версии бота.
Команды бота

/start — начало взаимодействия с ботом, отображает доступные команды.
/login — вход в админ-панель для изменения настроек.
/logout — выход из админ-панели.
/input_ip — изменение IP-адреса сервера (доступно только после входа).
/status, /server_status — проверка текущего статуса сервера.
/info — отображение информации о сервере (IP-адрес, статус).
/release — информация о версии бота.
Настройка и использование

Запуск ботаЗапустите скрипт Python, указанный ниже. Убедитесь, что у вас установлены необходимые библиотеки (telebot, requests, ntplib, pytz) и настроены токены API Telegram.
АвторизацияИспользуйте команду /login, чтобы ввести пароль администратора. После успешной авторизации вам станут доступны дополнительные команды для изменения настроек.
Использование командДля проверки статуса сервера используйте команду /status. Чтобы изменить IP-адрес сервера, выполните команду /input_ip и следуйте инструкциям.
Далее создайте файлы ip.txt и login.txt бот сделан на русском прото поменяйте в его коде слова на ваш язык в переводчике
Для запуска этого бота вам понадобятся следующие библиотеки Python:
1. **PyTelegramBotAPI**: Основная библиотека для работы с Telegram API.
2. **Requests**: Библиотека для отправки HTTP-запросов.
3. **Ntplib**: Используется для синхронизации времени с NTP-серверами.
4. **Pytz**: Необходима для работы с временными зонами.

EN
Documentation for an ordinary user

What does this bot do?

This Telegram bot is designed to manage and monitor the status of the Minecraft server. The main features include checking the server status, changing the server IP address and getting information about the bot version.

Bot commands

/Start - the beginning of interaction with the bot, displays the available commands.

/Login — login to the admin panel to change the settings.

/Logout — exit from the admin panel.

/Input_ip — change of server IP address (available only after logging in).

/Status, /server_status — check the current server status.

/Info — display of server information (IP address, status).

/Release — information about the bot version.

Setting up and using

Launching the bot Run the Python script listed below. Make sure that you have the necessary libraries installed (telebot, requests, ntplib, pytz) and Telegram API tokens configured.

Authorization Use the /login command to enter the administrator password. After successful authorization, you will have access to additional commands to change the settings.

Using commands To check the status of the server, use the /status command. To change the IP address of the server, run the command /input_ip and follow the instructions.

Next, create the files ip.txt and login.txt bot made in Russian proto change the words in its code to your language in the translator

To run this bot, you will need the following Python libraries:

1. **PyTelegramBotAPI**: The main library for working with Telegram API.

2. **Requests**: Library for sending HTTP requests.

3. **Ntplib**: Used to synchronize time with NTP servers.

4. **Pytz**: Necessary for working with time zones.
