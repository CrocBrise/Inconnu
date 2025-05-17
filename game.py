from random import choice, randint

class Game():
    def __init__(self, list_word):
        self.player_dict = {}
        self.num_player = 0
        self.num = {
            "player" : 0,
            "undercover" : 0,
            "mr_white" : 0
            }
        self.word_list = list_word
        self.word = 0
        self.save_word = []
        self.word_random = (0, 0)

    def player_identity(self):
        #We ask how many players play
        while self.num_player <= 0:
            try:
                self.num_player = int(input("Entrez le nombre de joueur"))
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        #Let's enter their names
        player = ""
        print("\n")
        for i in range(self.num_player):
            try:
                player = str(input(f"Entrez le nom du joueur {i + 1}"))
            except ValueError:
                print("Veuillez entrer un pseudo valide.")
            while player in list(self.player_dict.keys()):
                print("Ce joueur existe déja")
                try:
                    player = str(input(f"Entrer le nom du joueur {i + 1}"))
                except ValueError:
                    print("Veuillez entrer un pseudo valide.")
            self.player_dict[player] = [0, 0, "", ""]
        print("\n")

    def how_role(self):
        self.num["undercover"] = self.num_player + 1
        while self.num["undercover"] + self.num["mr_white"] >= self.num_player:
            try:    
                self.num["undercover"] = int(input("Entrez le nombre d'undercover"))
                self.num["mr_white"] = int(input("Entrez le nombre de monsieur White"))
            except ValueError:
                print("Entrez un nombre valide")
            if self.num["undercover"] + self.num["mr_white"] >= self.num_player:
                print(f"Attention, le nombre d'undercover et de monsieur White ne doit pas excéder {self.num_player - 1}")
        self.num["player"] = self.num_player - (self.num["undercover"] + self.num["mr_white"])

    def give_role(self, role :str, dict1:dict, dict2:dict):
        while self.num[role] > 0:
            rand_player = choice(list(dict2.keys()))
            dict1[rand_player] = role
            del dict2[rand_player]
            self.num[role] -= 1


    def new_tour(self):
        dic_return = {}
        player_dict_clone = {}
        for player in self.player_dict:
            player_dict_clone[player] = self.player_dict[player][0]
        rand_player = choice(list(player_dict_clone.keys()))
        del player_dict_clone[rand_player]
        if choice([True, False, True]) and self.num["undercover"] > 0:
            dic_return[rand_player] = "undercover"
            self.num["undercover"] -= 1
        else:
            dic_return[rand_player] = "normal"
        rand_player = 0
        while self.num["undercover"] > 0:
            rand_player = choice(list(player_dict_clone.keys()))
            dic_return[rand_player] = "undercover"
            del player_dict_clone[rand_player]
            self.num["undercover"] -= 1
        while self.num["mr_white"] > 0:
            rand_player = choice(list(player_dict_clone.keys()))
            dic_return[rand_player] = "mr_white"
            del player_dict_clone[rand_player]
            self.num["mr_white"] -= 1
        for player in player_dict_clone.keys():
            rand_player = randint(1, len(dic_return))
            dic_return[player] = "normal"
        n = 0
        for player in dic_return.keys():
            n += 1
            self.player_dict[player][1] = n
            self.player_dict[player][2] = dic_return[player]
    
    def choose_word(self):
        print("\n")
        word_random = self.word_list[randint(0, len(self.word_list) - 1)]
        word_role = randint(0, 1)
        while word_random in self.save_word:
            word_random = self.word_list[randint(0, len(self.word_list) - 1)]
        word_random = (word_random[word_role], word_random[1 if word_role == 0 else 0])
        self.save_word.append(word_random)
        for player in self.player_dict.keys():
            if self.player_dict[player][2] == "normal":
                self.player_dict[player][3] = word_random[0]
            elif self.player_dict[player][2] == "undercover":
                self.player_dict[player][3] = word_random[1]
            elif self.player_dict[player][2] == "mr_white":
                self.player_dict[player][3] = "[Aucun mot - vous êtes Mr_White]"


    def print_word(self):
        for player in self.player_dict:
            input(f"{player} - Prêt pour voir votre mot?")
            print("\n" * 35)
            print(f"{player} votre mot est {self.player_dict[player][3]}")
            input("Passez au joueur suivant")
            print("\n" * 35)
        self.player_dict = dict(sorted(self.player_dict.items(), key=lambda item: item[1][1]))
        input("Appuyer pour commencer le tour")
        print("\n" * 35)

    def add_player(self, player_entry):
        name = player_entry
        if name not in self.player_dict:
            self.player_dict[name] = [0, 0, "", ""]
            print(f"Le joueur {name} a été ajouté")
        else:
            print("Ce joueur existe déjà")

    def delete_player(self, player):
        if player in self.player_dict:
            print(f"Le joueur {player} a été supprimé - Il possédait {self.player_dict[player][0]} points")
            del self.player_dict[player]
        else:
            print("Merci d'entrer un nom compris dans la liste des joueurs actuels :")
            for player in self.player_dict:
                print(player)

    def classement(self):
        print("\n")
        meilleur_score = dict(sorted(self.player_dict.items(), key=lambda item: item[1][0], reverse=True))
        a = 0
        for player, liste in meilleur_score.items():
            a += 1
            print(f"{a} - {liste[0]} points - {player}")

    def winner_detector(self, ig):
        winner = "undercover"
        tour = not all(self.player_dict[player][2] == "normal" for player in ig)
        if tour:
            if len(ig) <= 2:
                tour = False
            else:
                tour = any(self.player_dict[player][2] == "normal" for player in ig)
        else:
            winner = "normal"
        return winner, tour

    def lobby(self):
        self.classement()
        response = 0
        while response != 5:
            response = 0
            while response not in (1, 2, 3, 4, 5, 6):
                print("\n  📇  * Menu *  📇  ")
                print("1 - Ajouter un joueur (avec 0 point)")
                print("2 - Retirer un joueur")
                print("3 - Afficher le classement")
                print("4 - Montrer les mots déja sortis")
                print("5 - Jouer un nouveau tour")
                print("6 - Finir le jeu")
                try:
                    response = int(input("Entrez votre action\n"))
                except ValueError:
                    print("Entrez un nombre valide")
            if response == 1:
                try:
                    self.add_player(str(input("Entrez le joueur à ajouter")))
                except ValueError:
                    print("Entrez un pseudo valide")
            elif response == 2:
                try:
                    self.delete_player(str(input("Entrez le joueur à supprimé")))
                except ValueError:
                    print("Entrez un pseudo valide")
            elif response == 3:
                self.classement()
            elif response == 4:
                print("\nListe des mots selon la forme : Normal - Undercover")
                for word in self.save_word:
                    print(f"{word[0]} - {word[1]}")
            elif response == 6:
                self.classement()
                return False
        return True
                
