import random
from time import sleep
from readchar import readchar

from data import game_state, load_data
from core import utils, battle, map
from data.game_state import MAP_HEIGHT, MAP_WIDTH

# VARIABLES >
rock_done = False
water_done = False
electric_done = False
fighting_done = False
locations_true = False
game_true = False
true_1 = False
true_2 = False
true_3 = False
true_4 = False
true_5 = False
true_6 = False
playing = True
limiter = 0
new_position = None
rock_gym = None
water_gym = None
electric_gym = None
fighting_gym = None
hospital_1 = None
hospital_2 = None
locations = []

## snake
POS_X = 0 # pos 1* of list
POS_Y = 1 # pos 2* of list

# < VARIABLES
def get_trainer_by_name(name):
    """
    Busca y devuelve el entrenador cuyo nombre coincida (sin distinción de mayúsculas/minúsculas)
    en la lista 'trainers'. Si no se encuentra, retorna None.
    """
    for trainer in game_state.trainers:
        if trainer.name.lower() == name.lower():
            return trainer
    return None

def intro(pokemon):
    location = ""
    while location not in ["1", "2", "3", "4"]:
        print(
            f"(i) Hospitals [H] restores HP\n"
            f"(i) WASD to move\n\n"
            f"{pokemon.name} {pokemon.hp} HP            LVL {pokemon.level}\n"
            f"{utils.message_life_indicator(pokemon)}\n"
        )

        # Listamos los ataques dinámicamente
        print(f"{pokemon.name} knows the following movements:")
        for attack in pokemon.attacks:
            print(f"  - {attack.name}")

        location = input(
            "Where are you coming from:\n  North (1)\n  South (2)\n  East  (3)\n  West  (4)\n\n"
        )
        utils.limpiar_pantalla()

        match location:
            case "1":
                my_position = [
                    random.randint(0, MAP_WIDTH - 1), random.randint(0, round(MAP_HEIGHT - ((MAP_HEIGHT - 1) / 1.5))),
                ]
            case "2":
                my_position = [
                    random.randint(0, MAP_WIDTH - 1), random.randint(round((MAP_HEIGHT + 1) / 1.5), MAP_HEIGHT - 1),
                ]
            case "3":
                my_position = [
                    random.randint(round((MAP_WIDTH + 1) / 1.5), MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1),
                ]
            case "4":
                my_position = [
                    random.randint(0, round(MAP_WIDTH - ((MAP_WIDTH - 1) / 1.5))), random.randint(0, MAP_HEIGHT - 1),
                ]
    return my_position

def time_battle_end(): # time
    sleep(2)


if __name__ == '__main__':
    load_data.load_data()

    player = game_state.user
    rock_brock = get_trainer_by_name("Brock")
    water_misty = get_trainer_by_name("Misty")
    electric_lt_surge = get_trainer_by_name("Lt. Surge")
    fighting_sabrina = get_trainer_by_name("Sabrina")


    obstacles = map.obstacles_creation()
    my_position = intro(player.pokemons[0])

    while not locations_true: # Locations creation
        while 0 <= limiter <= 5: 
            new_location = [random.randint(0, MAP_WIDTH -1), random.randint(0, MAP_HEIGHT -1)]
            if new_location not in locations and new_location != my_position and obstacles[new_location[POS_Y]][new_location[POS_X]] != ",":
                locations.append(new_location)
                if limiter == 0: # Rock Gym
                    water_gym = new_location
                    true_1 = True
                elif limiter == 1: # Water Gym
                    rock_gym = new_location
                    true_2 = True
                elif limiter == 2: # Electric Gym
                    electric_gym = new_location
                    true_3 = True
                elif limiter == 3: # Fighting Gym
                    fighting_gym = new_location
                    true_4 = True
                elif limiter == 4: # Hospital 1
                    hospital_1 = new_location
                    true_5 = True
                elif limiter == 5: # Hospital 2
                    hospital_2 = new_location
                    true_6 = True
                limiter += 1
            if true_1 and true_2 and true_3 and true_4 and true_5 and true_6:
                locations_true = True
        true_1 = False; true_2 = False; true_3 = False; true_4 = False; true_5 = False; true_6 = False; limiter = 0

    while not game_true:
        utils.limpiar_pantalla()
        # DRAW MAP >
        print("-"*(MAP_WIDTH* 2 + 3)) # Top

        for coordinate_y in range(MAP_HEIGHT): # Map and Fights
            print("|", end="") # left side

            for coordinate_x in range(MAP_WIDTH):
                char_to_draw = "  "

                # LOCATIONS PRINT >
                if rock_gym[POS_X] == coordinate_x and rock_gym[POS_Y] == coordinate_y: # rock gym print
                    char_to_draw = " R"
                if water_gym[POS_X] == coordinate_x and water_gym[POS_Y] == coordinate_y: # water gym print
                    char_to_draw = " W"
                if electric_gym[POS_X] == coordinate_x and electric_gym[POS_Y] == coordinate_y: # electric gym print
                    char_to_draw = " E"
                if fighting_gym[POS_X] == coordinate_x and fighting_gym[POS_Y] == coordinate_y: # fighting gym print
                    char_to_draw = " F"
                if hospital_1[POS_X] == coordinate_x and hospital_1[POS_Y] == coordinate_y: # hospital 1 print
                    char_to_draw = " H"
                if hospital_2[POS_X] == coordinate_x and hospital_2[POS_Y] == coordinate_y: # hospital 2 print
                    char_to_draw = " H"
                # < LOCATIONS PRINT

                # YOU >
                if my_position[POS_X] == coordinate_x and my_position[POS_Y] == coordinate_y: # your position
                    char_to_draw = " @" # you

                    if hospital_1[POS_X] == coordinate_x and hospital_1[POS_Y] == coordinate_y: # enter hospital 1
                        true_1 = True
                    if hospital_2[POS_X] == coordinate_x and hospital_2[POS_Y] == coordinate_y: # enter hospital 2
                        true_1 = True

                    # GYMS FIGHTS >
                    if not water_done: # Water Gym

                        if water_gym[POS_X] == coordinate_x and water_gym[POS_Y] == coordinate_y:
                            print(); utils.limpiar_pantalla(); input("You entered -Cerulean Water Gym-\n\n"); utils.limpiar_pantalla()

                            while not water_done: # water gym fight

                                if player.pokemons[0].hp > 0:
                                    my_turn = None
                                    while my_turn not in ["1", "2", "3", "4", "exit"]:
                                        utils.message_battle_starts(player.pokemons[0], water_misty.pokemons[0])
                                        my_turn = input(utils.message_pokemon_attacks(player.pokemons[0])); utils.limpiar_pantalla()

                                    if my_turn == "1":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[0], water_misty.pokemons[0])
                                    elif my_turn == "2":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[1], water_misty.pokemons[0])
                                    elif my_turn == "3":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[2], water_misty.pokemons[0])
                                    elif my_turn == "4":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[3], water_misty.pokemons[0])
                                    elif my_turn == "exit":
                                        game_true = True; water_done = True; playing = False
                                    time_battle_end(); utils.limpiar_pantalla()

                                if playing:
                                    if water_misty.pokemons[0].hp > 0:
                                        turn = random.randint(1, 4)

                                        if turn == 1:
                                            battle.damages(water_misty.pokemons[0], water_misty.pokemons[0].attacks[0], player.pokemons[0])
                                        elif turn == 2:
                                            battle.damages(water_misty.pokemons[0], water_misty.pokemons[0].attacks[1], player.pokemons[0])
                                        elif turn == 3:
                                            battle.damages(water_misty.pokemons[0], water_misty.pokemons[0].attacks[2], player.pokemons[0])
                                        elif turn == 4:
                                            battle.damages(water_misty.pokemons[0], water_misty.pokemons[0].attacks[3], player.pokemons[0])
                                        time_battle_end(); utils.limpiar_pantalla()

                                if water_misty.pokemons[0].hp < 1:
                                    true_2 = True
                                    water_done = True

                                    player.pokemons[0].max_hp += random.randint(6, 12)
                                    player.pokemons[0].damage += 1
                                    player.pokemons[0].level += 3

                                    # pikachu_critical = ((pikachu_critical * 10) + 1)/10
                                    # nuzzle["damage"] = int((pikachu["damage"]) * 2.5)
                                    # thunder_shock["damage"] = int((pikachu["damage"]) * 4.5)
                                    # quick_attack["damage"] = int((pikachu["damage"]) * 4)
                                    # feint["damage"] = int((pikachu["damage"]) * 3)
                                elif player.pokemons[0].hp < 1:
                                    true_3 = True
                                    water_done = True

                    if not rock_done: # Rock Gym

                        if rock_gym[POS_X] == coordinate_x and rock_gym[POS_Y] == coordinate_y:
                            print(); utils.limpiar_pantalla(); input("You entered -Pewter Rock Gym-\n\n"); utils.limpiar_pantalla()

                            while not rock_done: # rock gym fight

                                if player.pokemons[0].hp > 0:
                                    my_turn = None
                                    while my_turn not in ["1", "2", "3", "4", "exit"]:
                                        utils.message_battle_starts(player.pokemons[0], rock_brock.pokemons[0])
                                        my_turn = input(utils.message_pokemon_attacks(player.pokemons[0])); utils.limpiar_pantalla()

                                    if my_turn == "1":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[0], rock_brock.pokemons[0])
                                    elif my_turn == "2":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[1], rock_brock.pokemons[0])
                                    elif my_turn == "3":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[2], rock_brock.pokemons[0])
                                    elif my_turn == "4":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[3], rock_brock.pokemons[0])
                                    elif my_turn == "exit":
                                        game_true = True; rock_done = True; playing = False
                                    time_battle_end(); utils.limpiar_pantalla()

                                if playing:
                                    if rock_brock.pokemons[0].hp > 0:
                                        turn = random.randint(1, 4)

                                        if turn == 1:
                                            battle.damages(rock_brock.pokemons[0], rock_brock.pokemons[0].attacks[0], player.pokemons[0])
                                        elif turn == 2:
                                            battle.damages(rock_brock.pokemons[0], rock_brock.pokemons[0].attacks[1], player.pokemons[0])
                                        elif turn == 3:
                                            battle.damages(rock_brock.pokemons[0], rock_brock.pokemons[0].attacks[2], player.pokemons[0])
                                        elif turn == 4:
                                            battle.damages(rock_brock.pokemons[0], rock_brock.pokemons[0].attacks[3], player.pokemons[0])
                                        time_battle_end(); utils.limpiar_pantalla()

                                if rock_brock.pokemons[0].hp < 1:
                                    true_2 = True
                                    rock_done = True

                                    player.pokemons[0].max_hp += random.randint(7, 13)
                                    player.pokemons[0].damage += 1
                                    player.pokemons[0].level += 3

                                    # pikachu_critical = ((pikachu_critical * 10) + 1)/10
                                    # nuzzle["damage"] = int((pikachu["damage"]) * 2.5)
                                    # thunder_shock["damage"] = int((pikachu["damage"]) * 4.5)
                                    # quick_attack["damage"] = int((pikachu["damage"]) * 4)
                                    # feint["damage"] = int((pikachu["damage"]) * 3)
                                elif player.pokemons[0].hp < 1:
                                    true_3 = True
                                    rock_done = True

                    if not electric_done: # Electric Gym

                        if electric_gym[POS_X] == coordinate_x and electric_gym[POS_Y] == coordinate_y:
                            print(); utils.limpiar_pantalla(); input("You entered -Vermilion Electric Gym-\n\n"); utils.limpiar_pantalla()

                            while not electric_done: # electric gym fight

                                if player.pokemons[0].hp > 0:
                                    my_turn = None
                                    while my_turn not in ["1", "2", "3", "4", "exit"]:
                                        utils.message_battle_starts(player.pokemons[0], electric_lt_surge.pokemons[0])
                                        my_turn = input(utils.message_pokemon_attacks(player.pokemons[0])); utils.limpiar_pantalla()

                                    if my_turn == "1":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[0], electric_lt_surge.pokemons[0])
                                    elif my_turn == "2":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[1], electric_lt_surge.pokemons[0])
                                    elif my_turn == "3":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[2], electric_lt_surge.pokemons[0])
                                    elif my_turn == "4":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[3], electric_lt_surge.pokemons[0])
                                    elif my_turn == "exit":
                                        game_true = True; electric_done = True; playing = False
                                    time_battle_end(); utils.limpiar_pantalla()

                                if playing:
                                    if electric_lt_surge.pokemons[0].hp > 0:
                                        turn = random.randint(1, 4)

                                        if turn == 1:
                                            battle.damages(electric_lt_surge.pokemons[0], electric_lt_surge.pokemons[0].attacks[0], player.pokemons[0])
                                        elif turn == 2:
                                            battle.damages(electric_lt_surge.pokemons[0], electric_lt_surge.pokemons[0].attacks[1], player.pokemons[0])
                                        elif turn == 3:
                                            battle.damages(electric_lt_surge.pokemons[0], electric_lt_surge.pokemons[0].attacks[2], player.pokemons[0])
                                        elif turn == 4:
                                            battle.damages(electric_lt_surge.pokemons[0], electric_lt_surge.pokemons[0].attacks[3], player.pokemons[0])
                                        time_battle_end(); utils.limpiar_pantalla()

                                if electric_lt_surge.pokemons[0].hp < 1:
                                    true_2 = True
                                    electric_done = True

                                    player.pokemons[0].max_hp += random.randint(8, 14)
                                    player.pokemons[0].damage += 2
                                    player.pokemons[0].level += 3

                                    # pikachu_critical = ((pikachu_critical * 10) + 1)/10
                                    # nuzzle["damage"] = int((pikachu["damage"]) * 2.5)
                                    # thunder_shock["damage"] = int((pikachu["damage"]) * 4.5)
                                    # quick_attack["damage"] = int((pikachu["damage"]) * 4)
                                    # feint["damage"] = int((pikachu["damage"]) * 3)
                                elif player.pokemons[0].hp < 1:
                                    true_3 = True
                                    electric_done = True

                    if not fighting_done: # Fighting Gym

                        if fighting_gym[POS_X] == coordinate_x and fighting_gym[POS_Y] == coordinate_y:
                            print(); utils.limpiar_pantalla(); input("You entered -Cianwood Fighting Gym\n\n"); utils.limpiar_pantalla()

                            while not fighting_done: # fighting gym fight

                                if player.pokemons[0].hp > 0:
                                    my_turn = None
                                    while my_turn not in ["1", "2", "3", "4", "exit"]:
                                        utils.message_battle_starts(player.pokemons[0], fighting_sabrina.pokemons[0])
                                        my_turn = input(utils.message_pokemon_attacks(player.pokemons[0])); utils.limpiar_pantalla()

                                    if my_turn == "1":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[0], fighting_sabrina.pokemons[0])
                                    elif my_turn == "2":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[1], fighting_sabrina.pokemons[0])
                                    elif my_turn == "3":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[2], fighting_sabrina.pokemons[0])
                                    elif my_turn == "4":
                                        battle.damages(player.pokemons[0], player.pokemons[0].attacks[3], fighting_sabrina.pokemons[0])
                                    elif my_turn == "exit":
                                        game_true = True; fighting_done = True; playing = False
                                    time_battle_end(); utils.limpiar_pantalla()

                                if playing:
                                    if fighting_sabrina.pokemons[0].hp > 0:
                                        turn = random.randint(1, 4)

                                        if turn == 1:
                                            battle.damages(fighting_sabrina.pokemons[0], fighting_sabrina.pokemons[0].attacks[0], player.pokemons[0])
                                        elif turn == 2:
                                            battle.damages(fighting_sabrina.pokemons[0], fighting_sabrina.pokemons[0].attacks[1], player.pokemons[0])
                                        elif turn == 3:
                                            battle.damages(fighting_sabrina.pokemons[0], fighting_sabrina.pokemons[0].attacks[2], player.pokemons[0])
                                        elif turn == 4:
                                            battle.damages(fighting_sabrina.pokemons[0], fighting_sabrina.pokemons[0].attacks[3], player.pokemons[0])
                                        time_battle_end(); utils.limpiar_pantalla()

                                if fighting_sabrina.pokemons[0].hp < 1:
                                    true_2 = True
                                    fighting_done = True

                                    player.pokemons[0].max_hp += random.randint(10, 16)
                                    player.pokemons[0].damage += 2
                                    player.pokemons[0].level += 3

                                    # pikachu_critical = ((pikachu_critical * 10) + 1)/10
                                    # nuzzle["damage"] = int((pikachu["damage"]) * 2.5)
                                    # thunder_shock["damage"] = int((pikachu["damage"]) * 4.5)
                                    # quick_attack["damage"] = int((pikachu["damage"]) * 4)
                                    # feint["damage"] = int((pikachu["damage"]) * 3)
                                elif player.pokemons[0].hp < 1:
                                    true_3 = True
                                    fighting_done = True
        
                    # < GYMS FIGHTS
                # < YOU

                # WALLS PRINT >
                if obstacles[coordinate_y][coordinate_x] == ",": # Walls
                    if obstacles[my_position[POS_Y]][my_position[POS_X]] == ",": # don't draw walls on you
                        obstacles[my_position[POS_Y]][my_position[POS_X]] = " "
                    if obstacles[my_position[POS_Y]][my_position[POS_X]] != ",": # walls print
                        char_to_draw = " #"
                # < WALLS PRINT

                print("{}".format(char_to_draw), end="") # Printer
            print(" |") # right side

        print("-"*(MAP_WIDTH* 2 + 3)) # Bottom
        # < DRAW MAP

        # CONDITIONS >
        if true_1: # Hospital
            player.pokemons[0].hp = player.pokemons[0].max_hp
            print(); utils.limpiar_pantalla()
            print(f"{player.pokemons[0].name}'s HP Restored\n\nMove to Continue\n")
            true_1 = False
        if true_2: # Gym win
            utils.limpiar_pantalla(); print(f"{player.pokemons[0].name} grew to LVL {player.pokemons[0].level - 2}!\n"
                                f"{player.pokemons[0].name} grew to LVL {player.pokemons[0].level - 1}!\n"
                                f"{player.pokemons[0].name} grew to LVL {player.pokemons[0].level}!\n\n"
                                "Gym Cleared\n\nMove to Continue\n")
            true_2 = False
        if true_3: # Gym lost
            utils.limpiar_pantalla(); print("Gym Fight Losed\n\nYou Lose\n")
            game_true = True
        if rock_done and water_done and electric_done and fighting_done: # win conditions
            utils.limpiar_pantalla(); print("Congratulations! You win all battles!\n\nYou Win!\n")
            game_true = True
        if not playing: # exit game
            print(); utils.limpiar_pantalla()
        # < CONDITIONS

        if not game_true and not true_3:
            direction = readchar() # where player want to move

            if direction.upper() == "W" or direction.upper() == "5": # up movement
                new_position = [my_position[POS_X], my_position[POS_Y] - 1]
                if new_position[POS_Y] < 0:
                    new_position[POS_Y] = MAP_HEIGHT - 1

            elif direction.upper() == "S" or direction.upper() == "2": # down movement
                new_position = [my_position[POS_X], my_position[POS_Y] + 1]
                if new_position[POS_Y] > MAP_HEIGHT - 1:
                    new_position[POS_Y] = 0

            elif direction.upper() == "A" or direction.upper() == "1": # left movement
                new_position = [my_position[POS_X] - 1, my_position[POS_Y]]
                if new_position[POS_X] < 0:
                    new_position[POS_X] = MAP_WIDTH - 1

            elif direction.upper() == "D" or direction.upper() == "3": # right movement
                new_position = [my_position[POS_X] + 1, my_position[POS_Y]]
                if new_position[POS_X] > MAP_WIDTH - 1:
                    new_position[POS_X] = 0

            elif direction.upper() == "P": # right movement
                game_true = True

            if new_position: # in-game movement
                if obstacles[new_position[POS_Y]][new_position[POS_X]] != ",":
                    my_position = new_position

    # End