# Vk streaming api 

Streaming API — это инструмент для получения публичных данных из ВКонтакте по заданным ключевым словам. 

>**Обратите внимание, Streaming API доступен в режиме бета-тестирования. Документация может изменяться и дополняться по мере развития инструмента.**

Работа со Streaming API выглядит так — Вы проходите авторизацию, добавляете нужные Вам правила и затем получаете данные, которые подходят под эти правила, в едином потоке.

С помощью Streaming API Вы можете получить не более 1% всех публичных данных, удовлетворяющих заданным правилам. Чтобы получить доступ к расширенной версии Streaming API, включающей 100% данных, пожалуйста, свяжитесь с vk по этому адресу e-mail: [api@vk.com](mailto:api@vk.com), указав в качестве темы «Streaming API». Обратите внимание, что документация соответствует базовой версии Streaming API, и некоторые возможности расширенной версии здесь не описаны.

![Python 2.7, 3.4, 3.5, 3.6](https://img.shields.io/pypi/pyversions/vkstreaming.svg) ![v0.2.1](https://img.shields.io/pypi/v/vkstreaming.svg)

## Установка

```bash
pip install vkstreaming
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

### `upgrade_rules(list)`

Удаляет все правила и добавляет правила из списка `list`

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

[Список ошибок](https://vk.com/dev/streaming_api_docs_2?f=8.%20Сообщения%20об%20ошибках)

```python
try:
    ...
except VkError as e:
    print(e.error_code) #Код ошибки
    print(e.message) #Сообщение
```

