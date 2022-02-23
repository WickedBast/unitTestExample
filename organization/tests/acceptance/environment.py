import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unitTest.settings')
django.setup()

from behave import fixture, use_fixture
from django.contrib.auth.models import User
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from organization.models import Organization


class BaseTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser(username='admin', password='admin123456', email='ogul@vivadrive.io')

        User.objects.create(username='theCOO', password='dinesh123456', email='dinesh@vivadrive.io',
                            first_name='Dinesh', last_name='Kumar', is_active=True, is_staff=True)
        Organization.objects.create(name="VivaDrive", registration_code="V1v4Dr1v3",
                                    established_on="2004-04-04", address="Warsaw, Poland")
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        User.objects.filter().delete()
        super(BaseTestCase, cls).tearDownClass()


@fixture
def django_test_case(context):
    context.test_case = BaseTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    context.selenium.quit()
    del context.test_case


def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)
