# run_simulate.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monopoly_api.settings')
django.setup()

from games.services import run_and_save_simulation

run_and_save_simulation()
