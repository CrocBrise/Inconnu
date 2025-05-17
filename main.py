import csv
from random import choice, randint
from game import Game

def load_word(file_name):
    """Transforms a csv file into a python list

    Args:
        file_name (csv): A csv file

    Returns:
        table (list): A python list with words who are in csv file
    """
    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        table = csv.reader(file)
        table = [list(line) for line in table]
    return table


word = load_word("link_word.csv")
game = Game(word)
running = True
game.player_identity()
while running:
    a = 0
    game.how_role()
    game.new_tour()
    game.choose_word()
    game.print_word()
    ig = []
    for player in game.player_dict:
        ig.append(player)
    tour = True
    while tour:
        a += 1
        print(f"\n⚠️  Tour n°{a} ⚠️")
        print("L'ordre des joueurs est :")
        b = 0
        for player in ig:
            b += 1
            print(f"{b} - {player}")
        eliminate = ""
        while not eliminate in ig:
            try: 
                eliminate = str(input("\nEntrez le joueur qui a été éliminé"))
            except ValueError:
                print("Veuillez entrez un pseudo valide")
        ig.remove(eliminate)
        print(f"Le joueur {eliminate} était {game.player_dict[eliminate][2]}")
        tour = False
        winner, tour = game.winner_detector(ig)
        
    print("\n")
    if winner == "normal":
        print("Félicitations, les normaux ont gagnés la partie.")
        for liste in game.player_dict.values():
            if liste[2] == "normal":
                liste[0] += 1
    elif winner == "undercover":
        print("Félicitations, les undercovers ont gagnés la partie.")
        for liste in game.player_dict.values():
            if liste[2] in ("undercover", "mr_white"):
                liste[0] += 1
    print("\n" * 2)
    print("🕵️  Les rôles de cette partie 🕵️")
    for player in game.player_dict:
        print(f"Le joueur {player} était {game.player_dict[player][2]}")
    running = game.lobby()
