 
import os
import subprocess
import json
from .models import GameResult, PlayerData

def run_and_save_simulation():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jar_path = os.path.join(base_dir, "simulations", "MonopolySimulation.jar")

    result = subprocess.run(["java", "-jar", jar_path], capture_output=True, text=True)

    print("=== STDOUT ===")
    print(result.stdout)
    print("=== STDERR ===")
    print(result.stderr)
    if result.returncode == 0:
        try:
            # simulation_data = json.loads(result.stdout)
            lines = result.stdout.strip().splitlines()
            json_str = lines[-1]  # last line only
            simulation_data = json.loads(json_str)


            game = GameResult.objects.create(
                winner=simulation_data['winner'],
                strategy=simulation_data['strategy'],
                turns=simulation_data['turns']
            )

            for player in simulation_data['players']:
                PlayerData.objects.create(
                    game=game,
                    name=player['name'],
                    money=player['money'],
                    strategy=player['strategy']
                )

            print("Simulation and players saved successfully!")

        except json.JSONDecodeError:
            print("Error: Output is not valid JSON.")
            print(result.stdout)

    else:
        print("Simulation failed to run.")
        print(result.stderr)
