# -*- coding: utf-8 -*-
from vkstreaming import Streaming


if __name__ == '__main__':
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