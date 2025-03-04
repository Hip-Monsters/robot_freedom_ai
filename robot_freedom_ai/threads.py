# -*- coding: utf-8 -*-
"""
Description: Generic Daemon.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 8.0
Plaftorm: RaspberryPi
License: MIT License  
"""

from threading import Thread


def first_function(first_argu):
    print(first_argu)
    return "Return Value from " + first_argu


class AgentThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)

    def run(self):
        if self._target != None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


thread_1 = NewThread(target=first_function, args=("Thread 1",))
thread_2 = NewThread(target=first_function, args=("Thread 2",))

thread_1.start()

print(thread_1.join())