#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv

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
    # 檢查環境變數來區分開發和生產環境
    if os.getenv('DJANGO_ENV') == 'production':
        print("PRODUCTION")
    else:
        # 如果不是生產環境，讀取 .env 文件
        dotenv.read_dotenv()
        print("DEV")

    main()