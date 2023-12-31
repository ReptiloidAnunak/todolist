# **TODOLIST app**

**_Стек:_** _python3.9, Django, Postgres_

**Описание:**

Приложение представляет собой планировщик задач, который позволяет рационально распределять свое время.

**Функционал**

На данном этапе были реализованы следующие функции:

1. Вход/регистрация/аутентификация через вк.
2. Создание целей.
    Выбор временного интервала цели с отображением кол-ва дней до завершения цели.
    Выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории.
    Выбор приоритета цели (статичный список minor, major, critical и т. п.).
    Выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве).
3. Изменение целей.
    Изменение описания цели.
    Изменение статуса.
    Дать возможность менять приоритет и категорию у цели.
4. Удаление цели.
    При удалении цель меняет статус на «в архиве».
5. Поиск по названию цели.
6. Фильтрация по статусу, категории, приоритету, дедлайну.
7. Заметки к целям.
8. Все перечисленный функции должны быть реализованы в мобильном приложении.
9. Один пользователь может создавать сколько угодно досок
10. Внутри каждой доски свой набор категорий, целей, комментариев
11. Категории, цели, комментарии нельзя переносить из одной доски в другую
12. Реализованы права доступа для пользователей на чтение и изменение доски

Актуальная версия размещена на сайте http://reptiloidanunak.site

**Телеграм-бот**
1. Привязывает аккаунт телеграм-пользователя к его аккаунту в приложении с помощью верификационного кода
2. По команде пользователя выдает актуальный список его целей 
3. Позволяет создать новую цель

**Локальный запуск приложения**

1. Установить необходимые пакеты с помощью команды `pip install -r requirements.txt`
2. Установить docker в случае его отсутствия
3. Запустить команду `docker compose up -d`
4. Открыть ссылку: http://127.0.0.1/auth
5. Отправить сообщение телеграм-боту https://t.me/todolistreptil_bot, аутентифицироваться в приложении с помощью верификационного кода.

В случае проблем с запуском контейнера в терминале запустить следующие команды:
1. `docker compose down`
2. `sudo systemctl stop docker`
3. `sudo systemctl start docker`
4. `lsof -i :5432 | sudo ss -lptn 'sport = :5432'`
5. `sudo kill <pid>` 
6. `sudo service apache2 stop`
7. `docker compose up -d`

Обновление вольюмов при внесении правок в код:
1. `docker system prune -af`
2. `docker volume prune -f`
3. Посмотреть логи ошибок: `docker compose logs -f api`
