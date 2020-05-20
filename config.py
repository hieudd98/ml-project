import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    threshold=0.3
    bs=256
    model_path = '/home/dle/vi-lm/models/hsd_clas'
    data_path = '/home/dle/archives/hsd/data'
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = 'this-really-needs-to-be-changed'
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
