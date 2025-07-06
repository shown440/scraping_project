#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from django.core.management.commands.runserver import Command as runserver

from scraping_project.settings import BASE_DIR





def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping_project.settings_local')
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
    with open(BASE_DIR / 'env.json', 'r') as envf:
        env_ = json.load(envf)

    runserver.default_addr = env_['appconf']['default']['HOST']
    runserver.default_port = env_['appconf']['default']['PORT']
    
    main()
