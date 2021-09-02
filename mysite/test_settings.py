from mysite.settings import *
from django.test.runner import DiscoverRunner
from ponder import tests
from django.apps import apps
import sys

class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

class UnManagedModelTestRunner(DiscoverRunner):

    def setup_test_environment(self, *args, **kwargs):
        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)
 
    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        for m in self.unmanaged_models:
            m._meta.managed = False

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    
    DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
    DATABASES['default']['NAME'] = '<LOCAL_DATABASE_NAME>'
    DATABASES['default']['USER'] = '<YOUR_LOCAL_DATABASE_USER>'
    DATABASES['default']['PASSWORD'] = '<YOUR_LOCAL_DATABASE_USER_PASSWORD>'
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['PORT'] = '3306'

 
DATABASE_ROUTERS = []

MIGRATION_MODULES = DisableMigrations()

TEST_RUNNER = 'mysite.test_settings.UnManagedModelTestRunner'
