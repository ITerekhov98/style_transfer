## Тг бот, меняющий стиль фотографий с помощью нейросети

## Установка

Скачайте код, и перейдите в каталог проекта. Затем создайте файл `.env` и положите в него следующие параметры в формате `Ключ=значение`:
```
-TG_BOT_TOKEN - Токен вашего бота
-IMAGE_SIZE - Размер изображений, которые ваш бот будет генерировать
```
 По умолчанию `IMAGE_SIZE`= 256, при отсутствии GPU с таким значением генерация изображения займёт около минуты.
 
Установите необходимые зависимости:
```
pip3 install -r requirements.txt
```
Далее вам понадобится установить PyTorch. Его метод установки зависит от вашей OC, а также конфигурации устройства, поэтому он не включем в `requirements.txt`. Перейдите на [официальный сайт](https://pytorch.org/get-started/locally/) и проследуйте их инструкциям.

## Запуск

```
python tg_bot.py 
```
Первый запуск займёт чуть больше времени, так как скрипт будет загружать необходимые веса для модели.


## Пример работы:
### Исходное изображение
![gitcontent](https://user-images.githubusercontent.com/105926440/175781067-82d31efb-2d52-4e04-992e-a5a345458db7.jpg)

### Стиль
![gitstyle](https://user-images.githubusercontent.com/105926440/175781092-84949e24-4818-4265-b8b2-9c6219962311.jpg)
### Результат
![gitresult](https://user-images.githubusercontent.com/105926440/175781100-0d1d21dd-281f-4f9f-a6e7-ab4ccb70c26a.jpg)

[Источник картинки](https://www.treeoftheyear.org/Previous-Years/2020/Carodejny-strom.aspx?lang=ru-RU)
