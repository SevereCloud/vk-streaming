# vk streaming api ![Python 2.7, 3.4, 3.5, 3.6](https://img.shields.io/pypi/pyversions/vk_api.svg)

**Обратите внимание, Streaming API доступен в режиме бета-тестирования. Документация может изменяться и дополняться по мере развития инструмента.**

* [Документация](https://vk.com/dev/streaming_api_docs)
* [Получить ключ](https://vk.com/dev/streaming.getServerUrl)
* [Примеры использования](./examples)

## Установка

```bash
pip install vkstreaming
```

## Пример

```python
from vkstreaming import Streaming

api = Streaming("streaming.vk.com", "<key>")

rules = api.get_rules()
for rule in rules:
    print(("{tag:15}:{value}").format(**rule))

@api.stream
def my_func(event):
    print("[{}]: {}".format(event['author']['id'], event['text']))

api.start()
```

## Методы

**`get_rules()`** - Возвращает правила в виде массива
```json
[{"tag":"1","value":"коты"},{"tag":"2","value":"и"}]
```

**`add_rules(tag, value)`** - Добавить правило `value` с меткой `tag`

**`del_rules(tag)`** - Удалить правило с меткой `tag`

**`del_all_rules()`** - Удалить все правила

**`upgrade_rules(array)`** - Обновляет правила

## Стриминг

**`@api.stream`** - Декоратор. Во время стриминга вызывает метод с событием.

```python
@api.stream
def func(event):
    pass
```

**`start()`** - Запустить стриминг

**`stop()`** - Остановить стриминг

## Обработка исключений

[Список ошибок](https://vk.com/dev/streaming_api_docs_2?f=8.%20Сообщения%20об%20ошибках)

```python
try:
    ...
except VkError as e:
    print(e.error_code) #Код ошибки
    print(e.message) #Сообщение
```

