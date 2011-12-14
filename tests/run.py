# -*- coding: utf-8 -*-

import sys, os
from django.conf import settings


test_settings = {
    'ROOT_URLCONF': 'tests.test_app.urls',
    'INSTALLED_APPS': [
        'superview',
        'tests.test_app',
    ]
}


if __name__ == '__main__':
    test_args = sys.argv[1:]

    current_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    sys.path.insert(0, current_path)
    if not settings.configured:
        settings.configure(**test_settings)


    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=2, interactive=True, failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)

