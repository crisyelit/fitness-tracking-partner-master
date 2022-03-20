from django.contrib.auth import get_user_model
from faker import Faker
from random import randint, choice, sample
from .models import *
import psycopg2


class CategorySeed:

    model = Category

    @classmethod
    def seed(cls, **kwargs):
        
        default_categories = [
            {
                'name': 'Desarrollo', 
                'icon_class': 'development', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
            },
            {
                'name': 'Marketing', 
                'icon_class': 'marketing', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
            },
            {
                'name': 'Diseño gráfico', 
                'icon_class': 'graphic-design', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
            },
        ]

        result = []

        for item in default_categories:
            category = cls.model.objects.create(**item)
            result.append(category)

        return result

class SubCategorySeed:

    model = SubCategory
    category_model = Category

    @classmethod
    def seed(cls, **kwargs):
        fake = Faker()
        result = []

        for _ in range(0, randint(10, 15)):
            name = fake.text(max_nb_chars=randint(15, 25))
            description = fake.text(max_nb_chars=randint(15, 25))
            categories = cls.category_model.objects.all()

            data = {
                "name": name,
                "parent": choice(categories),
                "description": description,
            }

            result.append(cls.model.objects.create(**data))

        return result

class LanguageSeed:

    model = Language

    @classmethod
    def seed(cls, **kwargs):
        default_languages = [
            {
                'name': 'Español',
            },
            {
                'name': 'Ingles',
            },
        ]

        result = []

        for item in default_languages:
            result.append(cls.model.objects.create(**item))

        return result

class GroupSeed:

    model = Group
    category_model = Category
    sub_category_model = SubCategory
    tag_model = Tag
    language_model = Language
    user_model = get_user_model()

    @classmethod
    def populate(cls, group):
        users = cls.user_model.objects.filter(user_type='student')
        users = sample(list(users), randint(1, len(users)))

        group.following.add(*users)
        group.save()

        return group


    @classmethod
    def seed(cls, **kwargs):
        fake = Faker()
        result = []

        for _ in range(0, randint(10, 20)):
            title = fake.paragraph(nb_sentences=2)
            description = fake.paragraph(nb_sentences=7)
            short_description = fake.paragraph(nb_sentences=2)
            categories = cls.category_model.objects.all()
            sub_categories = cls.sub_category_model.objects.all()
            # tags = cls.tag_model.objects.all()
            languages = cls.language_model.objects.all()
            users = cls.user_model.objects.filter(user_type='leader')
            status = ['active','paused']

            data = {
                "title": title,
                "user": choice(users),
                "description": description,
                "short_description": short_description,
                "category": choice(categories),
                "sub_category": choice(sub_categories),
                "language": choice(languages),
                "status": choice(status),
            }

            try:
                print('Predata', data)
                group = cls.model.objects.create(**data)
                group = cls.populate(group)
                
                result.append(group)
            except Exception as e:
                print(e, data)

        return result

class LessonSeed:

    model = Lesson
    group_model = Group
    user_model = get_user_model()

    @classmethod
    def populate(cls, lesson):
        
        users = cls.user_model.objects.order_by("?")
        users = users[:randint(1, len(users))]

        lesson.booking.add(*users)
        lesson.save()

        return lesson


    @classmethod
    def seed(cls, **kwargs):
        fake = Faker()
        result = []

        for group in cls.group_model.objects.all():
            for _ in range(0, randint(1, 20)):
                title = fake.paragraph(nb_sentences=2)
                description = fake.paragraph(nb_sentences=7)
                short_description = fake.paragraph(nb_sentences=2)
                status = ['active','paused']
                start_date = fake.date_time_this_month(before_now=True, after_now=True)

                data = {
                    "group": group,
                    "title": title,
                    "user": group.user,
                    "description": description,
                    "short_description": short_description,
                    "is_privated": random.choice([True, False]),
                    "url": "https://example.com",
                    "status": choice(status),
                    "start_date": start_date,
                }

                try:
                    print('Predata', data)
                    lesson = cls.model.objects.create(**data)
                    lesson = cls.populate(lesson)
                    
                    result.append(lesson)
                except Exception as e:
                    print(e, data)

        return result
