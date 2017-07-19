# -*- coding: utf-8 -*-
"""
@author: Daniil Suvorov
@contact: https://severecloud.me
"""

import json
import requests
import websocket


"""
максимальное количество правил — 10;
максимальное количество ключевых слов в правиле — 10;
максимальный размер правила в байтах — 4096;
максимальный размер метки правила (tag) в байтах — 256;
"""
MAX_RULES = 10
MAX_WORD_RULES = 10


def getServerUrl(access_token, proxy_host=None, proxy_port=None, ver="5.67"):
    """
    :param access_token: Токен
    Возвращает Хост для подключения к серверу и ключ доступа
    """
    proxies = None
    if proxy_host:
        proxies = {'https': proxy_host+':'+str(proxy_port)}

    url = "https://api.vk.com/method/streaming.getServerUrl?v=" + \
        ver + "&access_token=" + access_token
    response = requests.get(url, proxies=proxies).json()
    if 'error' in response:
        raise VkError(response['error']['error_code'],
                      response['error']['error_msg'])
    return response["response"]


class Streaming(object):
    """Класс"""
    def __init__(self, endpoint, key, proxy_host=None, proxy_port=None):
        """
        :param endpoint: Хост для подключения к серверу
        :param key: Ключ доступа
        :param proxy_host: Прокси хост
        :param proxy_port: Прокси порт
        """
        self.endpoint = endpoint
        self.key = key

        self.proxies = None
        self.proxy_host = proxy_host
        self.proxy_port = None
        if proxy_port:
            self.proxies = {'https': proxy_host+':'+str(proxy_port)}
            self.proxy_port = int(proxy_port)
        
        self.list_func = []
        self.ws = None

    def get_rules(self):
        """Возвращает правила в виде списка"""

        url = "https://{}/rules?key={}".format(self.endpoint, self.key)

        response = requests.get(url, proxies=self.proxies).json()

        if response['code'] != 200:
            raise VkError(response['error']['error_code'],
                          response['error']['message'])
        else:
            return response['rules']

    def add_rules(self, tag, value):
        """
        :param tag: Метка правила
        :param value: Cтроковое представление правила
        Добавить правило `value` с меткой `tag`
        """

        url = "https://{}/rules?key={}".format(self.endpoint, self.key)
        values = {"rule": {"value": value, "tag": tag}}

        response = requests.post(url, json=values, proxies=self.proxies).json()

        if response['code'] != 200:
            raise VkError(response['error']['error_code'],
                          response['error']['message'])

    def del_rules(self, tag):
        """
        :param tag: Метка правила
        Удалить правило с меткой `tag`
        """

        url = "https://{}/rules?key={}".format(self.endpoint, self.key)
        values = {"tag": tag}

        response = requests.delete(url, json=values, 
                                   proxies=self.proxies).json()

        if response['code'] != 200:
            raise VkError(response['error']['error_code'],
                          response['error']['message'])

    def del_all_rules(self):
        """Удалить все правила"""
        rules = self.get_rules()
        if rules:
            for item in rules:
                self.del_rules(item['tag'])

    def update_rules(self, array):
        """
        :param array: Список правил
        Удаляет все правила и добавляет правила из списка `array`
        """
        if len(array) > MAX_RULES:
            raise VkError(2006, "Too many rules")
        else:
            self.del_all_rules()
            for item in array:
                self.add_rules(item['tag'], item['value'])

    def stream(self, func):
        """Декоратор. Во время стриминга вызывает метод с событием."""
        self.list_func.append(func)

    def start(self):
        """Запустить стриминг"""
        er = False

        def on_message(ws, message):
            """WebSocket получаем сообщение"""
            message = json.loads(message)
            if message['code'] == 100:
                for func in self.list_func:
                    func(message['event'])
            else:
                ws.close()
                self.start()

        def on_error(ws, error):
            """WebSocket получаем ошибку"""
            
            er = True

        def on_close(ws):
            """WebSocket закрыт"""
            pass

        url = "://{}/stream?key={}".format(self.endpoint, self.key)
        if self.proxies:
            self.ws = websocket.WebSocketApp("wss" + url,
                                             on_message=on_message,
                                             on_error=on_error,
                                             on_close=on_close
                                             )
        else:
            self.ws = websocket.WebSocketApp("wss" + url,
                                             on_message=on_message,
                                             on_error=on_error,
                                             on_close=on_close
                                             )
        self.ws.run_forever(http_proxy_host=self.proxy_host,
                            http_proxy_port=self.proxy_port)

        if er:
            headers = {
                "Connection": "upgrade",
                "Upgrade": "websocket",
                "Sec-Websocket-Version": "13"
            }
            response = requests.get("https" + url, headers=headers,
                                    proxies=self.proxies).json()

            if response['code'] == 400:
                raise VkError(response['error']['error_code'],
                              response['error']['message'])
            else:
                self.start()

    def stop(self):
        """Остановить стриминг. Запускать в декорируемой функции"""
        self.ws.close()


class VkError(Exception):
    """Ошибка vk"""
    def __init__(self, error_code, message):
        """
        :param error_code: Код ошибки
        :param message: Сообщение
        """
        self.message, self.error_code = message, error_code

    def __str__(self):
        return "{}: {}".format(self.error_code, self.message)
