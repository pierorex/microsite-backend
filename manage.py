#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    django_env = os.getenv('DJANGO_ENV', '')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "microsite_backend.{}settings".format(django_env))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
