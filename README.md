# Vk streaming api 

Streaming API — это инструмент для получения публичных данных из ВКонтакте по заданным ключевым словам. 

>**Обратите внимание, Streaming API доступен в режиме бета-тестирования. Документация может изменяться и дополняться по мере развития инструмента.**

Работа со Streaming API выглядит так — Вы проходите авторизацию, добавляете нужные Вам правила и затем получаете данные, которые подходят под эти правила, в едином потоке.

С помощью Streaming API Вы можете получить не более 1% всех публичных данных, удовлетворяющих заданным правилам. Чтобы получить доступ к расширенной версии Streaming API, включающей 100% данных, пожалуйста, свяжитесь с vk по этому адресу e-mail: [api@vk.com](mailto:api@vk.com), указав в качестве темы «Streaming API». Обратите внимание, что документация соответствует базовой версии Streaming API, и некоторые возможности расширенной версии здесь не описаны.

### UPD

> Streaming API — больше, лучше, удобнее. Обо всём по порядку: 
>1. Теперь учитывается не только текст записи/комментария, но и названия вложений — найдётся всё, что Вам нужно. 
>2. Вы можете получать 100% выборки данных по фильтрам вплоть до ~1800000 событий в месяц. Для подключения этой возможности напишите в Поддержку: vk.com/support?act=new_api, указав API_ID Вашего приложения. 
>3. Появилась возможность добавлять минус-слова — запросы, которые должны быть исключены из выборки. 
>4. Количество ключевых слов и правил увеличено до 100 и 300 соответственно. 
>5. Добавлен метод https://vk.com/dev/streaming.getStats для получения статистики по доставке событий. 
>6. В объектах событий добавлены вложения. 

![Python 2, 3](https://img.shields.io/pypi/pyversions/vkstreaming.svg?style=flat-square) ![v0.4](https://img.shields.io/pypi/v/vkstreaming.svg?style=flat-square)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSevereCloud%2Fvk-streaming.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FSevereCloud%2Fvk-streaming?ref=badge_shield)

## Установка

```bash
pip install vkstreaming
```

Обновить

```bash
pip install --upgrade vkstreaming
```

## Пример

```python
from vkstreaming import Streaming

api = Streaming("streaming.vk.com", "<key>")

api.del_all_rules()
api.add_rules("Котики", "кот")

rules = api.get_rules()
for rule in rules:
    print(("{tag:15}:{value}").format(**rule))

@api.stream
def my_func(event):
    print("[{}]: {}".format(event['author']['id'], event['text']))

api.start()
```

## Ссылки

* [Документация на vk.com/dev](https://vk.com/dev/streaming_api_docs)
* [Получить ключ](https://vk.com/dev/streaming.getServerUrl)
* [Примеры использования](./examples)

# Документация

## Авторизация

Чтобы получить учётные данные, необходимые для начала работы, используйте страницу API [streaming.getServerUrl](https://vk.com/dev/streaming.getServerUrl). В качестве результата метод возвращает URL для дальнейших запросов в поле `endpoint` и ключ доступа в поле `key` (string). 

```python
response = getServerUrl(access_token)

api = Streaming(response["endpoint"], response["key"])
```

## Прокси

```python
response = getServerUrl(access_token, proxy_host, proxy_port)
api = Streaming(response["endpoint"], response["key"], proxy_host, proxy_port)
```

## Формат правил

Правило — это набор ключевых слов, наличие которых в тексте объекта означает, что объект попадёт в поток.
* Если слова указаны без двойных кавычек, поиск ведётся с упрощением (все словоформы, без учёта регистра).
* Для поиска по точному вхождению (с учётом регистра, словоформы и т.п.) каждое слово должно быть указано в двойных кавычках.
* Минус (-) перед ключевым словом исключит из выборки тексты, содержащие это слово. Правило не может состоять только из ключевых слов с минусом.

>Например, правилу кот будут соответствовать объекты с текстом "кот", "кОт", "Котик".  
Правилу "кот" из вышеперечисленных будет соответствовать только объект с текстом "кот".  
Правилу -"кот" будут соответствовать объекты, которые не содержат точную словоформу «кот».  
Правилу -собака будут соответствовать объекты, которые не содержат слово «собака» в любой форме.

У каждого правила есть значение (**value**) — собственно содержание правила, и метка (**tag**). Вместе с каждым объектом Вы будете получать список его меток, чтобы понимать, какому правилу этот объект соответствует. 

### Ограничения
* максимальное количество правил — 300;
* максимальное количество ключевых слов в правиле — 100;
* максимальный размер правила в байтах — 4096;
* максимальный размер метки правила (tag) в байтах — 256;


## Методы для работы с правилами

### `get_rules()`

Возвращает правила в виде списка

```python
>>> api.get_rules()
[{"tag":"1","value":"коты"}, {"tag":"2","value":"и"}]
```

### `add_rules(tag, value)`

Добавляет правило `value` с меткой `tag`

```python
api.add_rules("Навальный", "навальн")
```

### `del_rules(tag)`

Удаляет правило с меткой `tag`

### `del_all_rules()`

Удаляет все правила

### `update_rules(list)`

Удаляет все правила и добавляет правила из списка `list`

```python
list = [{"tag":"1","value":"коты"}, {"tag":"2","value":"и"}]
api.update_rules(list)
```

## Стриминг

### `@api.stream`

Декоратор. Во время стриминга вызывает метод с событием.

Пример:
```python
@api.stream
def func(event):
    pass
```

### `start()`

Запустить стриминг

### `stop()`

Остановить стриминг. Запускать в декорируемой функции

## Обработка исключений

```python
try:
    ...
except VkError as e:
    print(e.error_code) #Код ошибки
    print(e.message) #Сообщение
```

[Список ошибок](https://vk.com/dev/streaming_api_docs_2?f=8.%20Сообщения%20об%20ошибках)

| error_code | message                                | Описание                                                                |
|------------|----------------------------------------|-------------------------------------------------------------------------|
| 1000       | Upgrade to websocket expected          | Неверно переданы параметры для обновления соединения до WebSocket       |
| 1001       | Wrong http method                      | Неподдерживаемый HTTP-метод                                             |
| 1002       | Wrong content type                     | Ключ “Content-type” либо отсутствует, либо не равен ожидаемому значению |
| 1003       | Missing key                            | Отсутствует параметр "key"                                              |
| 1004       | Bad key                                | Неправильное значение параметра "key"                                   |
| 1005       | Bad stream id                          | Недопустимое значение параметра "stream_id" (для расширенной версии)    |
| 1006       | Connection already established         | Такое соединение уже установлено                                        |
| 2000       | Can't parse json                       | Не удалось распарсить JSON в теле запроса                               |
| 2001       | Tag already exist                      | Правило с таким tag уже присутствует в этом потоке                      |
| 2002       | Tag not exist                          | Правило с таким tag отсутствует в этом потоке                           |
| 2003       | Can't parse rule                       | Не удалось распарсить содержимое rule                                   |
| 2004       | Too many filters                       | Слишком много фильтров в одном правиле                                  |
| 2005       | Unbalanced quotes                      | Непарные кавычки                                                        |
| 2006       | Too many rules                         | Слишком много правил в этом потоке                                      |
| 2008	     | At least one positive filter should be | Должно быть хотя бы одно ключевое слово без минуса                      |


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSevereCloud%2Fvk-streaming.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FSevereCloud%2Fvk-streaming?ref=badge_large)