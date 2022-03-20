
from utils.dynamic_import import Dimport
from django.conf import settings


class Seed:

    seeds = settings.SEEDS

    @classmethod
    def generate(cls, app, model, **kwargs):

        if not app in cls.seeds:
            raise Exception('Invalid seed')

        seed_class = Dimport.get_class(cls.seeds[app], f'{model}Seed')

        return seed_class.seed(**kwargs)

    
