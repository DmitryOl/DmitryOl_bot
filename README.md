**О боте:**
@DmitryOl_bot

**Учится:**

  * вести учет расходов
  * трекер дел
  * записи 
  * записывать какие видео и кто запрашивал скачать
  * выдавать ошибку если файл превышает 50мб
  * записывать кто какие аудио с ютуба запрашивал

**Умеет:**

  * Определять на какой системе запущен /cmd
  * Отправлять серверу сообщения через "cmd "
  * подключаться к бд SQLite смотреть и делать записи
  * yt - переслать видео (в целях изучения библиотеки)
  * ym - пересылать аудио

**install**
* в конфиг файл добавить id клиента, можно узнать с пом-ю бота https://t.me/my_id_bot
* в конфиг добавить токен бота, выдается при создании бота через https://t.me/BotFather
* =================--------------------=================
* Python version 3.9
* #python3 -m venv venv 
* source venv/bin/activate
* pip install -r requirements.txt
<br>
<br>скопируйте файл tgBot.service в директорию /lib/systemd/system/ 
<br>systemctl daemon-reload 
<br>systemctl start tgBot
<br>systemctl enabler tgBot
<br>systemctl status tgBot


