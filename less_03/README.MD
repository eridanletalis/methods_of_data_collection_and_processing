- Файл main.py содержит главный цикл обработки. При его запуске будет задан запрос на поиск, количество страниц для просмотра.
Также будет позволено выбрать, перезаписывать ли заново таблицы или только добавлять новую информация (сейчас не реализовано).
- Файл mysql_drive.py обслуживает запросы к mysql. Для личного удосбства использовался SSH-туннель вместо удалённого подключения 
к базе данных.
- Файл mongo_drive.py аналогично предыдущему обслуживает mongoDB
- Файл supple_function.py содержит общие функции.
- Файл get_vac.py позволяет сделать запрос к одной из баз, чтобы выбрать вакансии по определённому условию.

Для mysql используется SQLAlchemy с драйвером mysqlclient-1.4.6-cp37-cp37m-win_amd64.whl под Windows10. Брал отсюда https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient%23mysqlclient 
- Версия mysql 5.7.29
- Версия mongodb 3.6.3

Базы данных установлены на Raspberry Pi3B с ОС Ubuntu 18.04 x64 Server for RPi3. Весь доступ к машине по ssh

<b>Важное про базы данных MySQL и русский текст!</b>

Чтобы текст вставлялся в базу, во-первых, нужно использовать ```encode('utf-8')```, во вторых, база данных должна быть создана с поддержкой формата <i>utf8mb4</i> или преобразована к нему такими командами: 

```sql

ALTER DATABASE test_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE test_db.vacancy CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
