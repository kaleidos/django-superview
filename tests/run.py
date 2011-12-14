# -*- coding: utf-8 -*-

import sys, os
from django.conf import settings


test_settings = {
    'DATABASES':{
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    'ROOT_URLCONF': 'test_app.urls',
    'INSTALLED_APPS': [
        'superview',
        'test_app',
    ],
    'SV_CSS_MENU_ACTIVE':'selected',
}


if __name__ == '__main__':
    test_args = sys.argv[1:]

    current_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    sys.path.insert(0, current_path)
    if not settings.configured:
        settings.configure(**test_settings)

    if not test_args:
        test_args = ['test_app']
    
    print 1
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=2, interactive=True, failfast=False)
    failures = runner.run_tests(test_args)
    print 2
    sys.exit(failures)
