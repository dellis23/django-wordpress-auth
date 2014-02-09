# Deprecated, can be removed
import os

APP_NAME = os.path.basename(os.path.abspath(os.path.join(__file__, os.path.pardir)))


class WordpressRouter(object):

    def db_for_read(self, model, **hints):
        "Point all operations on wordpress models to 'wordpress'"
        if model._meta.app_label == APP_NAME:
            return 'wordpress'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on wordpress models to 'wordpress'"
        if model._meta.app_label == APP_NAME:
            return 'wordpress'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in wordpress is involved"
        if obj1._meta.app_label == APP_NAME or obj2._meta.app_label == APP_NAME:
            return True
        return None

    def allow_syncdb(self, db, model):
        "We don't create the wordpress tables via Django."
        return model._meta.app_label != APP_NAME
