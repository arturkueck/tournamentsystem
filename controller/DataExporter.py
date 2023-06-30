import sqlite3


class DataExporter:
    def __int__(self):
        self.conn = sqlite3.connect("../Turnierdata.db")
        self.cursor = self.conn.cursor()

    def add_new_player(self, firstname, surname):
        # Überprüfen, ob ein Spieler mit dem Vor- und Nachnamen bereits vorhanden ist
        query = "SELECT COUNT(*) FROM Spieler WHERE vorname=? AND nachname=?"
        self.cursor.execute(query, (firstname, surname))
        result = self.cursor.fetchone()

        if result[0] > 0:
            print("Ein Spieler mit diesem Vor- und Nachnamen existiert bereits.")
            return

        # Spieler hinzufügen
        insert_query = "INSERT INTO Spieler (vorname, nachname) VALUES (?, ?)"
        self.cursor.execute(insert_query, (firstname, surname))
        self.conn.commit()

        print("Der Spieler wurde erfolgreich hinzugefügt.")

    def add_tournament(self, date, tournament_type, double_rounds):
        # Überprüfen, ob der angegebene Turniertyp vorhanden ist
        query = "SELECT typ_id_PK FROM Turniertyp WHERE typbenennung=?"
        self.cursor.execute(query, (tournament_type,))
        result = self.cursor.fetchone()

        if result is None:
            print("Der angegebene Turniertyp existiert nicht.")
            return

        typ_id = result[0]

        # Turnier hinzufügen
        insert_query = "INSERT INTO Turnier (typ_id_FK, doppelrunde, datum) VALUES (?, ?, ?)"
        self.cursor.execute(insert_query, (typ_id, double_rounds, date))
        self.conn.commit()

        print("Das Turnier wurde erfolgreich hinzugefügt.")

    def add_round(self, tournament_round, tournament_date, result_array):
        # Finde die turnier_id_PK für das gegebene tournament_date
        self.cursor.execute("SELECT turnier_id_PK FROM Turnier WHERE datum = ?", (tournament_date,))
        turnier_id = self.cursor.fetchone()[0]

        # Füge eine neue Runde in die Tabelle "Runde" ein
        self.cursor.execute("INSERT INTO Runde (runde, turnier_id_FK) VALUES (?, ?)",
                            (tournament_round, turnier_id))

        # Speichere die Änderungen
        self.conn.commit()

        # Füge die Ergebnisse in die Tabelle "Rundenergebnis" ein
        for result in result_array:
            spieler_weiss_FK = result[0]
            spieler_schwarz_FK = result[1]
            ergebnis = result[2]

            self.cursor.execute(
                "INSERT INTO Rundenergebnis (spieler_weiss_FK, spieler_schwarz_FK, turnier_id_FK, runde, ergebnis) VALUES (?, ?, ?, ?, ?)",
                (spieler_weiss_FK, spieler_schwarz_FK, turnier_id, tournament_round, ergebnis))

        # Speichere die Änderungen
        self.conn.commit()

    def delete_tournament(self, date):
        # Find the turnier_id_PK for the given tournament_date
        self.cursor.execute("SELECT turnier_id_PK FROM Turnier WHERE datum=?", (date,))
        turnier_id = self.cursor.fetchone()[0]

        # Delete entries from Rundenergebnis table
        query = "DELETE FROM Rundenergebnis WHERE turnier_id_FK=?"
        self.cursor.execute(query, (turnier_id,))

        # Delete entries from SpielerInTurnier table
        query = "DELETE FROM SpielerInTurnier WHERE turnier_id_FK=?"
        self.cursor.execute(query, (turnier_id,))

        # Delete the tournament entry
        query = "DELETE FROM Turnier WHERE turnier_id_PK=?"
        self.cursor.execute(query, (turnier_id,))

        self.conn.commit()
        print("Das Turnier wurde erfolgreich gelöscht.")

    def delete_round(self, tournament_round, tournament_date):
        self.cursor.execute("SELECT turnier_id_PK FROM Turnier WHERE datum=?", (tournament_date,))
        turnier_id = self.cursor.fetchone()[0]

        # Delete entries from Rundenergebnis table
        query = "DELETE FROM Rundenergebnis WHERE turnier_id_FK=? AND runde=?"
        self.cursor.execute(query, (turnier_id, tournament_round))

        # Delete the round entry
        query = "DELETE FROM Runde WHERE turnier_id_FK=? AND runde=?"
        self.cursor.execute(query, (turnier_id, tournament_round))

        self.conn.commit()
        print("Die Runde wurde erfolgreich gelöscht.")

    def get_leaderboard(self, tournament_type):
        # Check if the given tournament type exists
        query = "SELECT typ_id_PK FROM Turniertyp WHERE typbenennung=?"
        self.cursor.execute(query, (tournament_type,))
        result = self.cursor.fetchone()

        if result is None:
            print("Der angegebene Turniertyp existiert nicht.")
            return

        typ_id = result[0]

        # Retrieve the leaderboard for the specified tournament type
        query = "SELECT R.platzierung, S.vorname, S.nachname" \
                " FROM Rangliste R" \
                " JOIN Spieler S ON R.spieler_id_FK = S.spieler_id_PK" \
                " WHERE R.typ_id_FK = ? ORDER BY R.platzierung ASC"
        self.cursor.execute(query, (typ_id,))
        return self.cursor.fetchall()

    def update_leaderboard(self, tournament_type):
        # Check if the given tournament type exists
        query = "SELECT typ_id_PK FROM Turniertyp WHERE typbenennung=?"
        self.cursor.execute(query, (tournament_type,))
        result = self.cursor.fetchone()

        if result is None:
            print("Der angegebene Turniertyp existiert nicht.")
            return

        typ_id = result[0]

        # Retrieve tournament information and player scores
        query = "SELECT T.turnier_id_PK, T.doppelrunde, S.spieler_id_PK, S.vorname, S.nachname, SIT.punkte, R.runde" \
                " FROM SpielerInTurnier SIT" \
                " JOIN Turnier T ON SIT.turnier_id_FK = T.turnier_id_PK" \
                " JOIN Spieler S ON SIT.spieler_id_FK = S.spieler_id_PK" \
                " JOIN Runde R ON R.turnier_id_FK = T.turnier_id_PK" \
                " WHERE T.typ_id_FK = ?" \
                " ORDER BY T.turnier_id_PK, S.spieler_id_PK, R.runde"
        self.cursor.execute(query, (typ_id,))
        rows = self.cursor.fetchall()

        tournament_info = {}

        # Iterate over the rows and construct tournament information dictionary
        for row in rows:
            tournament_id, doppelrunde, player_id, vorname, nachname, punkte, runde = row

            if tournament_id not in tournament_info:
                tournament_info[tournament_id] = {
                    'doppelrunde': doppelrunde,
                    'players': {}
                }

            if player_id not in tournament_info[tournament_id]['players']:
                tournament_info[tournament_id]['players'][player_id] = {
                    'vorname': vorname,
                    'nachname': nachname,
                    'punkte': {}
                }

            tournament_info[tournament_id]['players'][player_id]['punkte'][runde] = punkte

        # Calculate percentage scores for each player
        player_scores = {}

        for tournament_id, info in tournament_info.items():
            for player_id, player_info in info['players'].items():
                total_points = sum(player_info['punkte'].values())
                total_rounds = len(player_info['punkte'])
                percentage_score = (total_points / total_rounds) * 100

                if player_id not in player_scores:
                    player_scores[player_id] = []

                player_scores[player_id].append(percentage_score)

        # Calculate average percentage scores across the best five tournaments
        player_average_scores = {}

        for player_id, scores in player_scores.items():
            best_scores = sorted(scores, reverse=True)[:5]
            average_score = sum(best_scores) / len(best_scores)
            player_average_scores[player_id] = average_score

        # Rank players based on average percentage scores
        ranked_players = sorted(player_average_scores.items(), key=lambda x: x[1], reverse=True)

        # Store the rankings in a table
        rankings = []

        for i, (player_id, score) in enumerate(ranked_players, start=1):
            rankings.append((player_id, typ_id, i))

        # Delete existing rankings for the given tournament type
        delete_query = "DELETE FROM Rangliste WHERE typ_id_FK = ?"
        self.cursor.execute(delete_query, (typ_id,))

        # Insert the rankings into the "Rangliste" table
        insert_query = "INSERT INTO Rangliste (spieler_id_FK, typ_id_FK, platzierung) VALUES (?, ?, ?)"
        self.cursor.executemany(insert_query, rankings)

        self.conn.commit()

        # Print the rankings table
        print("Spieler ID\tPlatzierung")
        for player_id, _, ranking in rankings:
            print(f"{player_id}\t\t{ranking}")

    def show_leaderboard(self, tournament_type):
        # Check if the given tournament type exists
        query = "SELECT typ_id_PK FROM Turniertyp WHERE typbenennung=?"
        self.cursor.execute(query, (tournament_type,))
        result = self.cursor.fetchone()

        if result is None:
            print("Der angegebene Turniertyp existiert nicht.")
            return

        typ_id = result[0]

        # Retrieve the leaderboard from the "Rangliste" table
        query = "SELECT S.spieler_id_PK, S.vorname, S.nachname, R.platzierung" \
                " FROM Rangliste R" \
                " JOIN Spieler S ON R.spieler_id_FK = S.spieler_id_PK" \
                " WHERE R.typ_id_FK = ?" \
                " ORDER BY R.platzierung"
        self.cursor.execute(query, (typ_id,))
        leaderboard = self.cursor.fetchall()

        # Print the leaderboard table
        print("Platzierung\tSpieler ID\tVorname\t\tNachname")
        for ranking, player_id, vorname, nachname in leaderboard:
            print(f"{ranking}\t\t{player_id}\t\t{vorname}\t\t{nachname}")

        return leaderboard
