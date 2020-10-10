# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread

import pyttsx3


class Tts(QThread):
    speed = 1

    def __init__(self):
        super(Tts, self).__init__()
        self.engine = pyttsx3.init()
        self.say_text = ''

    def run(self):
        while True:

            if self.say_text != '':
                self.engine.say(self.say_text)
                self.say_text = ''
                res = self.engine.runAndWait()
            self.msleep(100)

    def getProperty(self, key):
        self.engine.getProperty(key)

    def setProperty(self, key, value):
        self.engine.setProperty(key, value)

    def stoptts(self):
        if self.engine.isBusy():
            self.say_text = ''

    def say(self, p_str):
        # self.engine.stop()
        self.say_text = p_str

