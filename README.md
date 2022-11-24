**УСТАНОВКА И ЗАПУСК**
В директории /tagcounter выполнить pip install .
Помощь:
\tagcounter>tagcounter -h
usage: tagcounter [-h] [--get GET] [--view VIEW] [--add ADD [ADD ...]]
                  [--delete DELETE] [--synonyms]

Count tags in html.

optional arguments:
  -h, --help           show this help message and exit
  --get GET            get tag list, example: tagcounter --get
                       http://yandex.ru
  --view VIEW          view saved info about tags from database, example:
                       tagcounter --veiw http://yandex.ru
  --add ADD [ADD ...]  add synonym to synonyms.yaml, example: tagcounter --add
                       tst http://python.org
  --delete DELETE      delete synonym from synonyms.yaml example: tagcounter
                       --delete tst
  --synonyms           view synonyms.yaml

Посчитать теги на странице:
tagcounter --get yandex.ru
Адрес можно передавать в формате yandex.ru, www.yandex.ru, http://yandex.ru, http://www.yandex.ru

Синонимы хранятся в файле tagcounter/synonyms.yaml
Посмотреть сохраненные синонимы:
tagcounter --synonyms

Можно добавить или удалить синонимы.
Добавить:
tagcounter --add tst http://python.org
tst - синоним
http://python.org - url

Удалить синоним:
tagcounter --delete tst

Запустить юнит-тесты:
1) Перейти в директорию
tagcounter\package_tagcounter
2) выполнть команду 
python -m unittest tests.py
