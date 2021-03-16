# Minimus

Инструмент для ведения заметок по методу **Zettelkasten**.

В двух словах:
1. Пишете заметки в текстовых файлах, указываете в них теги.
1. Запускаете **minimus**.
1. Получаете сшивку связей в ваших заметках. 

## Что за **Zettelkasten**?

Этот метод был придуман немецким социологом 
[Никласом Луманом](https://ru.wikipedia.org/wiki/%D0%9B%D1%83%D0%BC%D0%B0%D0%BD,_%D0%9D%D0%B8%D0%BA%D0%BB%D0%B0%D1%81).

Метод строится на применении упорядоченного набора листков бумаги. 
Каждый листок должен быть пронумерован и содержать одну специфическую идею. 
Листки могут содержать ссылки друг на друга и обобщающие теги. 
Все листки хранятся в пронумерованных ящиках, за счёт чего листок с любым номером можно быстрой найти. 

Основные идеи:

1. Отсутствие категорий. Информация в системе хранится в виде графа, 
   введение каких-либо категорий не предусматривается. 
   За счёт этого проще добавлять информацию, не имеющую чётко определённой области.
2. Отсутствует проблема переполнения данными. 
   Система работает тем лучше, чем больше в ней информации.
3. Желательно использование максимально примитивных технологий. 
   Предполагается, что система создаётся один раз и на всю жизнь, 
   поэтому не должно быть зависимости от конкретного приложения, 
   формата или чего-то подобного.
4. Желательно максимальное количество ссылок в системе. 
   Информация, не сцепленная с другими заметками, скорее всего будет бесполезна.
5. Ничего не удаляется. При пересмотре содержимого лучше добавлять заметки, 
   описывающие, почему предыдущие были неправильными.

Набор этих простейших правил создаёт очень удобную и максимально живучую систему сохранения знаний.

## Для чего это приложение

Чтобы было удобнее вести заметки. Оно сшивает заметки по тегам. 
Ещё он умеет создавать дополнительные страницы для тегов, чтобы было понятно, 
где они упоминаются. Предполагается, что архив заметок будет лежать в сетевом хранилище 
вроде Yandex Disk / Google drive / Dropbox. Для работы не требуются сторонние приложения и интернет.

Желательно при этом, чтобы каталог контролировался системой контроля версий, например git.

## Как пользоваться

Для пользователей:
   1. Скачать себе репозиторий: https://github.com/IgorZyktin/minimus/archive/master.zip, разархивировать.
   2. Положить свои заметки в каталог source (подробнее см. ниже).
   3. Запустить **run_RU.bat** или **run_EN.bat**.

Для разработчиков:
   1. Клонировать репозиторий.
   2. Положить свои заметки в каталог source.
   2. Вызвать python -m minimus.

Скрипт будет пытаться читать данные из подкаталога **source** и 
будет пытаться сохранять данные в каталог **target**. 
При желании можно подправить содержимое *.bat файлов, чтобы использовались другие каталоги.

### Начало работы

Надо создать несколько текстовых файлов с заметками в формате markdown. 
Расширение файлов должно быть ".md".
 
Желательный формат заметок:
```markdown
# Название заметки

Краткое описание

{{ тег номер один }}

{{ тег номер два }}

{{ тег номер три }}

## Заголовок

Текст, в котором может быть что-то про {{ тег номер два }} например.
```

Заголовком статьи будет считаться первое, что идёт после #. 
Тегами будет считаться всё, что нашлось в шапке документа, что идёт в формате {{ тег }}.
Теги можно писать в любом порядке, но категория записи будет определяться по
первому тегу. А стартовые страницы с перечнем всех материалов буду строиться только 
по категориям.

После этого можно запускать minimus. Если всё пройдёт хорошо, выходной текст будет:
```markdown
# Название заметки

Краткое описание

[тег номер один](./meta_teg_nomer_odin.md)

[тег номер два](./meta_teg_nomer_dva.md)

[тег номер три](./meta_teg_nomer_tri.md)

## Заголовок

Текст, в котором может быть что-то про [тег номер два](./meta_teg_nomer_dva.md) например.
```
Видно, что сам текст заметки остался тем же, но теперь теги это не просто 
текст, а реальные ссылки на другие документы.

### Посмотреть живьём

В репозиторий (и соответствующий [zip архив](https://github.com/IgorZyktin/minimus/archive/master.zip)) 
включены каталоги source и target, открыв их, можно посмотреть что из чего сгенерировалось и как выглядит.

### Аргументы запуска

  Ключ | Значение
:--------------------------------------:|:-----------------------------------:
--language RU                           | Язык примечаний ('RU' или 'EN')
--source_directory "C:\my cool folder"  | Выбрать каталог исходных данных
--target_directory "C:\my cool folder"  | Выбрать каталог для сохранения
--readme_directory "C:\my cool folder"  | Выбрать каталог для файла README.md
 
### Развёртывание

Я храню на компьютере bat файл со скриптом запуска. 
Он позволяет мне быстро пересобрать новую версию заметок.

```batch
@ECHO off
SET base=C:\Users\MainUser\YandexDisk
SET source=zettelkasten_source\content
SET target=zettelkasten_target\content
SET readme=zettelkasten_target
SET executable_directory=C:\PycharmProjects\minimus\
SET executable=%executable_directory%minimus.exe

CD %executable_directory%

%executable% ^
    --language RU ^
    --source_directory %base%\%source% ^
    --target_directory %base%\%target% ^
	--readme_directory %base%\%readme%

(echo Данный репозиторий был собран с помощью проекта Minimus: https://github.com/IgorZyktin/minimus) > %base%\%readme%\README.md.tmp
echo: >> %base%\%readme%\README.md.tmp
type %base%\%readme%\README.md >> %base%\%readme%\README.md.tmp
move /y %base%\%readme%\README.md.tmp %base%\%readme%\README.md

PAUSE
EXIT
```

### Справочные данные

1. Подробнее про **Zettelkasten**: 
    * http://vonoiral.com/all/zettelkasten/
    
1. Подробнее про **python** (на этом языке написан линковщик): 
    * https://pythonworld.ru/osnovy/skachat-python.html
    * Скачать тут: https://www.python.org/ftp/python/3.8.3/python-3.8.3.exe
    
1. Подробнее про **typora** (я применяю этот markdown редактор):
    * https://typora.io/
    * Скачать https://typora.io/#windows
    * Скачать https://typora.io/#linux
