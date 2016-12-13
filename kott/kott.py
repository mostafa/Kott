# -*- coding: utf-8 -*-
# TODO: KExceptoin, check data type,
"""docstring."""

from kcore.ksingleton import kSingleton
from kcore import krand
from kplugbase import KPlugBase

import md5
import time
import string
import random
import threading
import time
import sys
import os


@kSingleton
class Kott:
    __mem__ = {}
    __kplugs__ = []

    def __init__(self):
        pass

    def load_kplug(self, kplug_instance):
        self.__kplugs__.append(kplug_instance)
        self.__kplugs__.sort(lambda x, y: x.priority < y.priority)
        return kplug_instance.on_load()

    def get(self, key, **kwargs):
        value = self.__mem__[key]

        tp = type(value)
        for c_kplug in self.__kplugs__:
            if isinstance(value, c_kplug.data_type) and \
               c_kplug.has_keyword(**kwargs):
                value = c_kplug.on_get(key, value, **kwargs)

        return value

    def set(self, data, **kwargs):
        key = md5.md5(krand.kRandStr(16) + str(time.time())).hexdigest()
        for c_kplug in self.__kplugs__:
            if isinstance(data, c_kplug.data_type) and \
               c_kplug.has_keyword(**kwargs):
                data = c_kplug.on_set(key, data, **kwargs)
        self.__mem__[key] = data
        return key

    def pop(self, key, **kwargs):
        if key in self.__mem__:
            data = self.get(key, **kwargs)
            self.delete(key, **kwargs)
            return data
        return None

    def find(self, **kwargs):
        found_keys = []
        for key in self.__mem__:
            tp = type(self.__mem__[key])
            kplug_res = {}
            for c_kplug in self.__kplugs__:
                kplug_res[c_kplug] = True
                if isinstance(self.__mem__[key], c_kplug.data_type) and \
                   c_kplug.has_keyword(**kwargs):
                    kplug_res[c_kplug] = c_kplug.on_find_visit(key, self.__mem__[key], **kwargs)

            and_all = True
            for plug in kplug_res:
                and_all = and_all and kplug_res[plug]
            if and_all:
                found_keys.append(key)

        return found_keys

    def do(self, **kwargs):
        for key in self.__mem__:
            tp = type(self.__mem__[key])
            for c_kplug in self.__kplugs__:
                if isinstance(self.__mem__[key], c_kplug.data_type) and \
                   c_kplug.has_keyword(**kwargs):
                    c_kplug.on_do_visit(key, self.__mem__[key], **kwargs)

    def delete(self, key, **kwargs):
        if key in self.__mem__:
            self.__mem__.pop(key)

    def cleanup(self, **kwargs):
        self.__mem__ = {}
