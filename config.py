import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'


class DefaultConfig(Config):
    DEBUG = True
