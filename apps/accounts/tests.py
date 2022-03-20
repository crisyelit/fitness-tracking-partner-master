import shutil
import tempfile

from django.test import TestCase, override_settings

from .models import User

# Create your tests here.

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        user = {
            'username': 'testUser',
            'password': 'asdw1235',
            'email': 'testuser@ex.com',
            'first_name': "Pepe",
            'last_name': "Perez",
        }

        cls.user = User.objects.create_user(**user)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_it_has_information_fields(self):
        self.assertIsNotNone(self.user.image)
        self.assertIsNotNone(self.user.public_id)
