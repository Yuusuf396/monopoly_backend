# import os
# import django
# import json


# from django.db import connection
 

# # Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monopoly_api.settings')
# django.setup()

# from games.models import GameResult, PlayerData

# # Load JSON
# with open('new_all_results.json', 'r') as f:
#     data = json.load(f)

# GameResult.objects.all().delete()
# PlayerData.objects.all().delete()


# GameResult.objects.all().delete()
# PlayerData.objects.all().delete()

# # Reset primary key sequence (SQLite)
# with connection.cursor() as cursor:
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='games_gameresult';")
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='games_playerdata';")

# # Load into DB
# for entry in data:
#     game = GameResult.objects.create(
#         winner=entry['winner'],
#         strategy=entry['strategy'],
#         turns=entry['turns']
#     )

#     for player in entry['players']:
#         PlayerData.objects.create(
#             game=game,
#             name=player['name'],
#             money=player['money'],
#             strategy=player['strategy']
#         )

# print("✅ Loaded", len(data), "games into the database!")


import os
import django
import json
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monopoly_api.settings')
django.setup()

from games.models import GameResult, PlayerData

# Load JSON file
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new_all_results.json')
with open(json_path, 'r') as f:
    data = json.load(f)

# Delete old data
print("🗑️ Deleting all game data...")
PlayerData.objects.all().delete()
GameResult.objects.all().delete()

# Detect DB engine and reset sequences accordingly
db_engine = connection.settings_dict['ENGINE']

with connection.cursor() as cursor:
    if 'sqlite' in db_engine:
        print("🔁 Resetting SQLite sequences...")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='games_gameresult';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='games_playerdata';")
    elif 'postgresql' in db_engine:
        print("🔁 Resetting PostgreSQL sequences...")
        cursor.execute("ALTER SEQUENCE games_gameresult_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE games_playerdata_id_seq RESTART WITH 1;")
    else:
        print("⚠️ Sequence reset not implemented for this DB engine:", db_engine)

# Reload new data
print("📥 Loading new simulation data...")

for entry in data:
    game = GameResult.objects.create(
        winner=entry['winner'],
        strategy=entry['strategy'],
        turns=entry['turns']
    )

    for player in entry['players']:
        PlayerData.objects.create(
            game=game,
            name=player['name'],
            money=player['money'],
            strategy=player['strategy']
        )

print(f"✅ Loaded {len(data)} games into the database!")
