#!/usr/bin/python
#  singleton.py
#  helps make singleton object


class SingletonClass(object):
    """ A singleton class that can only be spawned once """

    # class variable that stores the instances of subclasses
    _instance = dict()

    # instanciate or return singleton
    def __new__(cls):
        try :
           object = cls._instance[cls]
           return object
        except KeyError:
             cls._instance[cls] = super(SingletonClass, cls).__new__(cls)
            return cls._instance[cls]