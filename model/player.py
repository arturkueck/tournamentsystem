class Player:
    def __init__(self, player_id, first_name, lastname, avg_placement, starting_position):
        self.player_id = player_id
        self.first_name = first_name
        self.lastname = lastname

        self.avg_placement = avg_placement
        self.place_in_tournament = starting_position
        self.plays_in_next_round = True

        self.points = 0
        self.buchholz = 0
        self.sbb = 0

        self.opponents = []

    def get_name(self):
        return self.first_name + " " + self.lastname

    def get_avg_placement(self):
        return self.avg_placement

    def get_place_in_tournament(self):
        return self.place_in_tournament

    def set_place_in_tournament(self, place):
        self.place_in_tournament = place

    def add_opponent(self, player_id, result):
        self.opponents.append(player_id, result)