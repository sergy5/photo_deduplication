```markdown
# Приложение для поиска и удаления дубликатов

## Установка

Для установки необходимых зависимостей выполните следующую команду:

```bash
pip install -r requirements.txt
```

## Использование

```bash
# Создание кэша файлов в заданной папке
python -X utf8 compute_md5.py --num_threads 1 /d/Фото /d/Фото/cache_md5.txt # если уже есть кэш, то вычисляется только для новых файлов

# Очистка кэша  от удаленных файлов
python -X utf8 clear_cache.py /d/Фото/cache_md5.txt

# Преобразовать /d/Фото/cache_md5.txt в utf-8 при необходимости

# Поиск файлов с одинаковыми файлами, подсчет их количества
python -X utf8 find_similar_folders.py /d/Фото/cache_md5.txt /d/Фото/similar_folders_list.txt 

# Перемещение одинаковых файлов в специальную корзину
python -X utf8 ./remove_duplicates.py /d/Фото/similar_folders_list.txt /d/Фото/cache_md5.txt
```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. файл `LICENSE`.

## Контакты

Author: Tushev Sergey
Email: sergy5@mail.ru  
GitHub: https://github.com/sergy5
GitVerse: https://gitverse.ru/tushev_sa
