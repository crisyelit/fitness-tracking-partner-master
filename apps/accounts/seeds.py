from faker import Faker
from .models import *
import random


class UserSeed:

    model = User

    @classmethod
    def set_parent(cls):
        
        coach = cls.model.objects.filter(user_type = 'coach').order_by("?")

        if len(coach) == 0:
            return False

        return coach.first()

    @classmethod
    def seed(cls, **kwargs):
        fake = Faker()
        user_type_choices = ['customer', 'coach']
        result = []

        for i in range(0, random.randint(10, 25)):
            profile = fake.simple_profile()

            try:
                first_name, last_name = profile.get('name').split(" ")
            except ValueError:
                continue

            user_type = random.choice(user_type_choices)

            data = {
                "username": profile.get('username'),
                "first_name": first_name,
                "last_name": last_name,
                "email" : profile.get('mail'),
                "user_type": user_type,
                "address": profile.get('username'),
                "password": 'example1235'
            }

            if user_type == 'customer':
                parent = cls.set_parent()
                if parent:
                    data['parent'] = parent
                else:
                    data['user_type'] = 'coach'


            result.append(cls.model.objects.create_user(**data))

        return result


class TestSeed:


    @classmethod
    def seed(cls, **kwargs):
        result = [
            {
                "msg": 'Works!',
            }
        ]

        return result

