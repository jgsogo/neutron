#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.utils.bots import DeepLinkingBot


class NeutronBot(DeepLinkingBot):
    def register_messages(self):
        self.message_handler(commands=['help'])(self.on_help)

    def on_help(self, message):
        msg = 'Muchas gracias por unirte al proyecto *Neutrón*. A través de la interfaz de Telegram puedes' \
              'colaborar aportando información, para ello utiliza:' \
              '\word Ayúdanos a identificar qué palabras son comunes en tu región.'
        self.send_message(message.chat.id, msg, parse_mode='Markdonw')