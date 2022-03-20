from django.core.management.base import BaseCommand, CommandError
from apps.core.seeds import Seed

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--application', type=str)
        parser.add_argument('--model', type=str)

    def handle(self, *args, **kwargs):  

        app = kwargs.get('application')
        model = kwargs.get('model')
        objects = Seed.generate(app, model)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(objects)}'))