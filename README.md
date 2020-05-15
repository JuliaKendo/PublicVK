### ПУБЛИКАЦИЯ КОМИКСОВ В "ВКОНТАКТЕ"
---

Данный скрип скачивает случайный комикс с сайта [https://xkcd.com](https://xkcd.com) и публикует его в сообществе [ВКонтакте](https://vk.com). При каждом запуске скрипта скачивается и публикуется один комикс.

Запускают скрипт без параметров
```
python.exe main.py
```	
В данной разработке инициализируются следующие переменные окружения:
- `VK_ACCESS_TOKEN` - переменная в которой хранится секретный токен, необходимый для подключения к api сайта [vk.com](http://www.vk.com). Для получения секретного токена рекомендуется использовать процедуру  [Implicit Flow](https://vk.com/dev/implicit_flow_user)

Данные переменные инициализируются значениями заданными в .env файле.

Информацию о ходе выполнения скрипт пишет в файл log.txt, который должен находится в корневой папке скрипта.

#### КАК УСТАНОВИТЬ
---

Для установки необходимо отредактировать файл .env, в котором заполнить `VK_ACCESS_TOKEN`.

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

#### ЦЕЛЬ ПРОЕКТА
---

Код написан в образовательных целях, для изучения возможностей api, на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
