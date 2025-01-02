#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv

DJANGO_ENV = "development"

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hulolo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    dotenv.read_dotenv('.env.common')
    if DJANGO_ENV == 'production':
        print("----PRODUCTION MODE----")
        dotenv.read_dotenv('.env.production', override=True)
    else:
        print("----DEV MODE----")
        dotenv.read_dotenv('.env.development', override=True)
    main()
