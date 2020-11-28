# Minimus

Инструмент для ведения заметок по методу **Zettelkasten**.

---

В двух словах:
1. Пишете заметки в текстовых файлах, указываете в них теги.
1. Запускаете **minimus**.
1. Получаете отображение связей в ваших заметках. 

Например вот так:

![logo]

[logo]: ./graph.gif "Пример графа заметок"

Пример использования на видео:

[![demo](https://img.youtube.com/vi/4UHA3SIrj8E/0.jpg)](https://www.youtube.com/watch?v=4UHA3SIrj8E)

## Что за **Zettelkasten**?

Этот метод был придуман немецким социологом [Никласом Луманом](https://ru.wikipedia.org/wiki/%D0%9B%D1%83%D0%BC%D0%B0%D0%BD,_%D0%9D%D0%B8%D0%BA%D0%BB%D0%B0%D1%81).

Метод строится на применении упорядоченного набора листков бумаги. Каждый листок должен быть пронумерован и содержать одну специфическую идею. Листки могут содержать ссылки друг на друга и обобщающие теги. По своей сути, зеттелькастен напоминает гипертекст. Все листки хранятся в пронумерованных ящиках, за счёт чего листок с любым номером можно быстрой найти. 

Основные идеи:

1. Отсутствии категорий. Информация в системе хранится в виде графа, введение каких-либо категорий не предусматривается. За счёт этого проще добавлять информацию, не имеющую чётко определённой области.
2. Отсутствует проблема переполнения данными. Система работает тем лучше, чем больше в ней информации.
3. Желательно использование максимально примитивных технологий. Предполагается, что система создаётся один раз и на всю жизнь, поэтому не должно быть зависимости от конкретного приложения, формата или чего то подобного.
4. Желательно максимальное количество ссылок в системе. Информация, не сцепленная с другими заметками не будет работать.
5. Ничего не удаляется. При пересмотре содержимого лучше добавлять заметки, описывающие, почему предыдущие были неправильными.

Набор этих простейших правил создаёт очень удобную и максимально живучую систему сохранения знаний.

## Для чего этот репозиторий

Чтобы было удобнее вести заметки. Автоматический линковщик сшивает заметки между собой по указанным в них тегам. Ещё он умеет создавать дополнительные страницы для тегов, чтобы было понятно, где они упоминаются.

В основе лежат две идеи:
1. Чем проще инструмент, тем выше шанс, что тебе будет не лень им пользоваться.
1. Сделать проще невозможно.

Серьёзно, что может быть проще пачки текстовых документов? Предполагается, что архив заметок будет лежать в сетевом хранилище вроде Yandex Disk / Google drive / Dropbox. Для работы не требуются сторонние приложения и интернет.

Желательно при этом, чтобы каталог контролировался системой контроля версий, например git.

## Как пользоваться

1. Скачать себе репозиторий: https://github.com/IgorZyktin/minimus/archive/master.zip, разархивировать.
2. Положить свои заметки в каталог source (подробнее см. ниже).
3. Если есть установленый python (3.6 и выше) - запустить **run_python.bat**.
4. Если нет python - запустить **run_RU.bat** или **run_EN.bat**.

Скрипт будет пытаться читать данные из подкаталога **source** и будет пытаться сохранять данные в каталог **target**. При желании можно подправить содержимое *.bat файлов, чтобы использовались другие каталоги.

### Начало работы

Надо создать несколько текстовых файлов с заметками в формате markdown. Расширение файлов должно быть ".md".
 
Желательный формат заметок:
```markdown
# Название заметки

Краткое описание

---

\\#тег номер один

\\#тег номер два

\\#тег номер три

## Заголовок

Текст, в котором может быть что-то про \#тег номер два например.
```

Заголовком статьи будет считаться первое, что идёт после октоторпа (#). Тегами будет считаться всё, что нашлось в шапке документа, что идёт после \\# без пробела и продолжается до конца строки. Линковщик умеет искать теги и в теле документа, но в первую очередь он опирается на перечисление тегов перед самим текстом заметки. Важно помнить, что у тегов нет завершающего символа, нельзя просто взять и понять где тег кончается. Поэтому они в примере приводятся каждый на своей строке.

После этого можно запускать линковщик. Если всё пройдёт хорошо, выходной текст будет:
```markdown
# Название заметки

Краткое описание

---

[\#тег номер один](./meta_teg_nomer_odin.md)

[\#тег номер два](./meta_teg_nomer_dva.md)

[\#тег номер три](./meta_teg_nomer_tri.md)

## Заголовок

Текст, в котором может быть что-то про [\#тег номер два](./meta_teg_nomer_dva.md) например.
```
Видно, что сам текст заметки остался тем же, но теперь теги это не просто текст, а реальные ссылки на другие документы.

### Что он делает

Линковщик просканирует все файлы в каталоге и:
1. Выполнит замену текста тегов на соответствующие им гиперссылки. md документы ссылаются на md документы, html на html.
1. Создаст метафайлы meta_*.md для каждого тега, где будет перечислено в каких документах этот тег упоминается.
1. Создаст метафайлы meta_*.html для каждого тега, где будет нарисовано облако из документов с этим тегом.
1. Создаст метафайл index.html, в котором будет граф из всех тегов и всех документов.
1. Создаст метафайл index.md, в котором будет список всех заметок.

Примерно вот так:
```
C:\folder>run_RU.bat
-------------------------------------------------------------------------------
Скрипт был запущен в каталоге: C:\folder
Каталог исходных данных: C:\folder\source
Каталог обработанных данных: C:\folder\target
Сборка будет произведена со стилем ссылок Local Explorer

Этап 1. Генерация метафайлов.
        01 из 10. Создан файл: C:\folder\target\meta_hobot.md
        02 из 10. Создан файл: C:\folder\target\meta_hobot.html
        03 из 10. Создан файл: C:\folder\target\meta_seryy.md
        04 из 10. Создан файл: C:\folder\target\meta_seryy.html
        05 из 10. Создан файл: C:\folder\target\meta_4_lapy.md
        06 из 10. Создан файл: C:\folder\target\meta_4_lapy.html
        07 из 10. Создан файл: C:\folder\target\meta_hvost.md
        08 из 10. Создан файл: C:\folder\target\meta_hvost.html
        09 из 10. Создан файл: C:\folder\target\meta_mashina.md
        10 из 10. Создан файл: C:\folder\target\meta_mashina.html

Этап 2. Генерация гиперссылок
        1 из 4 Был обновлён файл: 2020-07-06_elephant.md
        2 из 4 Был обновлён файл: 2020-07-06_mouse.md
        3 из 4 Был обновлён файл: 2020-07-06_recursion.md
        4 из 4 Был обновлён файл: 2020-07-06_vacuum.md

Этап 3. Генерация индексов
        Был создан файл: C:\folder\target\index.md
        Был создан файл: C:\folder\target\index.html

Этап 4. Сохранение основных файлов
        1 из 4. Сохранены изменения в файле C:\folder\target\2020-07-06_elephant.md
        2 из 4. Сохранены изменения в файле C:\folder\target\2020-07-06_mouse.md
        3 из 4. Сохранены изменения в файле C:\folder\target\2020-07-06_recursion.md
        4 из 4. Сохранены изменения в файле C:\folder\target\2020-07-06_vacuum.md

Этап 5. Сохранение дополнительных файлов

Этап 6. Копирование библиотек
        1 из 4. Скопирован файл C:\folder\minimus\arbor.js
        2 из 4. Скопирован файл C:\folder\minimus\jquery-3.5.1.min.js
        3 из 4. Скопирован файл C:\folder\minimus\rendering.js
        4 из 4. Скопирован файл C:\folder\minimus\utils.js
```
Важно помнить, что линковщик это не динамический инструмент. Он не нужен для чтения заметок, только для их сшивки. Достаточно время от времени запускать его при обновлении содержимого. Читать заметки при этом можно с любого устройства, python при этом не требуется. 

После внесения изменений в заметки, линковщик должен быть запущен повторно. Он опять создаст все мета документы и стартовую страницу. Предполагается, что в пределах нескольких тысяч заметок это будет работать достаточно быстро. 

Сразу после этого уже можно работать. Но пользоваться html документами будет не очень удобно т.к. бразуер будет открывать md документы просто как текст. Чтобы видеть разметку, необходимо расширение для браузера. В данном проекте применён Local Explorer (ссылка внизу). После его установки Chrome будет запускать md документы через стандартное приложение операционной системы.

### Посмотреть живьём

В репозиторий (и соответствующий [zip архив](https://github.com/IgorZyktin/minimus/archive/master.zip)) включены каталоги source и target, открыв их, можно посмотреть что из чего сгенерировалось и как выглядит.

### Аргументы запуска

  Ключ | Значение
:-----:|:---:
--lang  |  Язык примечаний ('RU' или 'EN')
--localexplorer  |  Сборка с генерацией ссылок в формате "Local Explorer"
--source_directory "C:\my cool folder"  | Выбрать каталог исходных данных
--target_directory "C:\my cool folder"  | Выбрать каталог для сохранения
 
### Развёртывание

Я храню на компьютере bat файл со скриптом запуска. 
Он позволяет мне быстро пересобрать новую версию заметок.

```batch
@ECHO off
SET source=C:\Users\MainUser\YandexDisk\zettelkasten_source\content
SET target=C:\Users\MainUser\YandexDisk\zettelkasten_target\content
SET executable_directory=C:\PycharmProjects\minimus\
SET executable=%executable_directory%minimus.exe

CD %executable_directory%

%executable% ^
    --lang RU ^
    --source_directory %source% ^
    --target_directory %target% ^
    --localexplorer

PAUSE
EXIT
```

### Справочные данные

1. Подробнее про **Zettelkasten**: 
    * http://vonoiral.com/all/zettelkasten/
    
1. Подробнее про **jQuery** (обеспечивает работу скриптов в данном проекте): 
    * https://jquery.com/
    * Скачать тут: https://jquery.com/download/
    
1. Подробнее про **arbor.js** (рисует графы в данном проекте): 
    * http://arborjs.org/
    * Скачать тут: http://arborjs.org/js/dist/arbor-v0.92.zip
    
1. Подробнее про **python** (на этом языке написан линковщик): 
    * https://pythonworld.ru/osnovy/skachat-python.html
    * Скачать тут: https://www.python.org/ftp/python/3.8.3/python-3.8.3.exe
    
1. Подробнее про **typora** (я применяю этот markdown редактор):
    * https://typora.io/
    * Скачать https://typora.io/#windows
    * Скачать https://typora.io/#linux
       
1. Подробнее про **Local Explorer** (позволяет открывать гиперссылки как файлы):
    * https://chrome.google.com/webstore/detail/local-explorer-file-manag/eokekhgpaakbkfkmjjcbffibkencdfkl
    * Скачать тут: http://goo.gl/trX9bB

### Над чем можно поработать

1. Иногда бывают сложности с кликами по узлам графа.
1. Формирование сложного графа возможно через костыль, когда имя тего совпадает с именем категории. Стоит улучшить связывание категорий между собой.
1. Не сохраняется положение узлов графа. При каждом открытии координаты генерируются случайно, поэтому приходится искать нужную категорию глазами. При попытке принудительно задать координаты на этапе создания страницы, в текущем варианте страница просто зависает.
1. Постоянно перезаписываются все файлы в целевом каталоге, даже те, что не были изменены. Пока это не сказалось на производительности, посмотрим, что будет с более крупными архивами заметок.
1. Периодически бывают конвульсии узлов графа. Вероятно стоит подкрутить настройки arbor.js.
1. Узлы гарфа нормально подчинаются при перетаскивании, но неадекватно себя ведут если в процессе перетаскивания перестать двигать мышью.
1. Не реализован выбор цветов связей и узлов.
1. Проект не выложен на PyPI.
1. Надо бы наделить первый тег в списке тегов большей важностью.