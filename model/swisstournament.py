class SwissTournament:
    def __init__(self, participant_list, round_count):
        self.round = 0
        self.round_count = round_count
        self.tournament_overview = []
        self.player_list = participant_list

    def create_tournament(self):
        # Sortiere die Spieler nach durchschnittlicher Platzierung
        self.player_list = sorted(self.player_list, key=lambda x: x.get_avg_placement())

    def add_player(self, player_id):
        # Füge den Spieler zur Turnierübersicht hinzu
        self.player_list.append(player_id)

    def remove_player(self, player_id):
        # Entferne den Spieler aus den Paarungen der nächsten Runde
        if player_id in self.player_list:
            self.player_list.remove(player_id)

    def update_player(self, player_id, points, buchholz, sbb):
        # Aktualisiere die Ergebnisse des Spielers
        for player in self.player_list:
            if player.player_id == player_id:
                player.points = points
                player.buchholz = buchholz
                player.sbb = sbb

    def sort_players(self):
        self.player_list = sorted(self.player_list, key=lambda x: (x.points, x.buchholz, x.ssb))

    def pairings_next_round(self):
        self.sort_players()
        half_of_players = int(len(self.player_list)/2) #obere Hälfte der Spieler

        for i in range(half_of_players):
            self.tournament_overview[self.round][i] = [
                self.player_list[(i % 2) * half_of_players + i].player_id,
                self.player_list[((i + 1) % 2) * half_of_players * i].player_id,
                0
            ]

        self.round = self.round + 1

    def show_round(self, round_num):
        # Filtere die Paarungen für die angegebene Runde
        round_pairings = [pair for pair in self.tournament_overview if pair[0] == round_num]

        # Ausgabe der Paarungen und Ergebnisse
        for pair in round_pairings:
            player1 = next((p for p in self.player_list if p.player_id == pair[1]), None)
            player2 = next((p for p in self.player_list if p.player_id == pair[2]), None)
            result = pair[3]
            if player1 and player2:
                print(f"Player {player1.get_name()} vs Player {player2.get_name()}: {result}")

    def finish_tournament(self):
        # Hier kannst du die Überprüfung und Datenbankübermittlung implementieren
        pass
