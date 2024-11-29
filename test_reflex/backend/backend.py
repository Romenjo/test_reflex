import reflex as rx
from .player import Player
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime
from .player import Player
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, select
from .data_items import all_items
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import psycopg2
import random
from psycopg2.sql import SQL, Identifier
from sqlalchemy.exc import SQLAlchemyError
import json
import os
from psycopg2.extras import DictCursor




class State(rx.State):
    """The app state."""

    players: list[Player] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    form_data: dict = {}

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    selected_items: Dict[str, List] = (
        all_items  
    )

    age: tuple[int, int] = (18, 44)
    market_value: tuple[int, int] = (0, 200000000)
    rating: tuple[float, float] = (2.0, 10.0)

    @rx.var(cache=True)
    def filtered_sorted_players(self) -> list[Player]:
        players = self.players

        # Filter players based on selected item
        if self.sort_value:
            # Sorting logic
            def get_sort_key(player):
                value = getattr(player, self.sort_value)
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return str(value).lower()

            players = sorted(
                players,
                key=get_sort_key,
                reverse=self.sort_reverse,
            )

        if self.search_value:
            search_value = self.search_value.lower()
            players = [
                player
                for player in players
                if any(
                    search_value in str(getattr(player, attr)).lower()
                    for attr in [
                        "name",
                        "team",
                        "position",
                        "nationality",
                        "age",
                        "height",
                        "games",
                        "goals",
                        "assists",
                        "average_rating",
                        "market_value",
                    ]
                )
            ]

        return players

    
    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Player]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_players[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def load_entries(self):
        db_connection_string = 'postgresql://postgres:asgard123@localhost/football'
        
        # Connect to the database
        def connect_to_db(db_connection_string):
            try:
                engine = create_engine(db_connection_string)
                print("Підключення до бази даних успішне!")
                return engine
            except Exception as e:
                print(f"Помилка підключення до бази даних: {e}")
                return None
        
        engine = connect_to_db(db_connection_string)

        if not engine:
            return []

        # SQL query to get the needed data along with player statistics
        query = """
        SELECT 
            players.player_id,
            players.name,
            clubs.name AS team,
            positions.position_name AS position,
            countries.country_name AS nationality,
            EXTRACT(YEAR FROM AGE(players.date_of_birth)) AS age,
            players.height_in_cm AS height,
            players.market_value_in_eur AS market_value,
            -- Aggregate the player statistics
            COALESCE(SUM(player_statistics.goals), 0) AS goals,
            COALESCE(SUM(player_statistics.assists), 0) AS assists,
            COALESCE(AVG(player_statistics.rating), 0) AS average_rating,
            -- Count the number of distinct games the player appeared in
            COUNT(DISTINCT player_statistics.game_id) AS games
        FROM players
        JOIN clubs ON players.current_club_id = clubs.club_id
        JOIN positions ON players.position_id = positions.position_id
        JOIN countries ON players.nationality_id = countries.country_id
        LEFT JOIN player_statistics ON players.player_id = player_statistics.player_id
        GROUP BY players.player_id, clubs.name, positions.position_name, countries.country_name
        """

        df = pd.read_sql(query, engine)

        players = []
        for _, row in df.iterrows():
            try:
                # Replace None or NaN with appropriate defaults
                height = int(row['height']) if pd.notna(row['height']) else 0
                market_value = f'{row["market_value"]:.2f}' if pd.notna(row['market_value']) else 'Unknown'
                age = int(row['age']) if pd.notna(row['age']) else 0
                # Format the average_rating to 2 decimal places, replace None with 0.0
                average_rating = round(row['average_rating'], 2) if pd.notna(row['average_rating']) else 0.0
                
                # Only include players with 10 or more games
                if row['games'] < 10:
                    continue  # Skip this player
                
                # Replace None/NaN values with 'Unknown' for string fields
                name = row['name'] if pd.notna(row['name']) else 'Unknown'
                team = row['team'] if pd.notna(row['team']) else 'Unknown'
                position = row['position'] if pd.notna(row['position']) else 'Unknown'
                nationality = row['nationality'] if pd.notna(row['nationality']) else 'Unknown'

                # Create Player object with the statistics included
                player = Player(
                    name=name,
                    team=team,
                    position=position,
                    nationality=nationality,
                    age=age,
                    height=height,
                    games=row['games'],  # Number of games played
                    goals=row['goals'],
                    assists=row['assists'],
                    average_rating=average_rating,  # Rounded to 2 decimal places
                    market_value=market_value
                )
                players.append(player)
            except ValueError as e:
                print(f"Error processing player {row['name']}: {e}")
                continue  # Skip players with invalid data

        # Set total items
        self.players = players  
        self.total_items = len(self.players)

        #print(players)
        #в цій функції я так розумію, ми якраз і маємо зробити мерджі
        #таблиць аби інфу про гравців витягнути і зберегти в 
        # players. а потім ці гравці будуть в табличці нашій відображені    


    @rx.var(cache=True)
    def get_age_value_chart_data(self) -> list[dict]:
        age_value_data = {}
        age_count = {}

        for player in self.players:
            if (
                not pd.isna(player.age)
                and not pd.isna(player.market_value)
                and player.team in self.selected_items["teams"]
                and player.position in self.selected_items["positions"]
                and self.age[0] <= player.age <= self.age[1]
                and self.rating[0] <= player.average_rating <= self.rating[1]
                and self.market_value[0] <= float(player.market_value) <= self.market_value[1]
            ):
                age = player.age
                if age not in age_value_data:
                    age_value_data[age] = 0
                    age_count[age] = 0

                age_value_data[age] += float(player.market_value)
                age_count[age] += 1

        return [
            {
                "age": age,
                "average value": round(
                    age_value_data.get(age, 0) / age_count.get(age, 1), 2
                ),
            }
            for age in range(self.age[0], self.age[1] + 1)  # Ensure we include all ages
        ]


    @rx.var(cache=True)
    def get_team_value_chart_data(self) -> list[dict]:
        team_value_data = {}
        team_count = {}

        for player in self.players:
            if (
                not pd.isna(player.team)
                and not pd.isna(player.market_value)
                and player.team in self.selected_items["teams"]
                and player.position in self.selected_items["positions"]
                and self.age[0] <= player.age <= self.age[1]
                and self.rating[0] <= player.average_rating <= self.rating[1]  
                and self.market_value[0] <= float(player.market_value) <= self.market_value[1]
            ):
                team = player.team
                if team not in team_value_data:
                    team_value_data[team] = 0
                    team_count[team] = 0

                team_value_data[team] += float(player.market_value)
                team_count[team] += 1

        return [
            {
                "team": team,
                "total value": team_value_data[team],
            }
            for team in team_value_data
        ]


    @rx.var(cache=True)
    def get_team_age_average_data(self) -> list[dict]:
        team_age_data = {}
        team_count = {}

        for player in self.players:
            if (
                not pd.isna(player.team)
                and not pd.isna(player.age)
                and player.team in self.selected_items["teams"]
                and player.position in self.selected_items["positions"]
                and self.age[0] <= player.age <= self.age[1]
                and self.rating[0] <= player.average_rating <= self.rating[1]
                and self.market_value[0] <= float(player.market_value) <= self.market_value[1]
            ):
                team = player.team
                if team not in team_age_data:
                    team_age_data[team] = []
                    team_count[team] = 0

                team_age_data[team].append(player.age)
                team_count[team] += 1

        return [
            {
                "team": team,
                "average age": round(sum(ages) / team_count[team], 2),
            }
            for team, ages in team_age_data.items()
        ]


    @rx.var(cache=True)
    def get_age_rating_chart_data(self) -> list[dict]:
        age_rating_data = {}
        age_count = {}

        for player in self.players:
            if (
                not pd.isna(player.age)
                and not pd.isna(player.market_value)
                and player.team in self.selected_items["teams"]
                and player.position in self.selected_items["positions"]
                and self.age[0] <= player.age <= self.age[1]
                and self.rating[0] <= player.average_rating <= self.rating[1]
                and self.market_value[0] <= float(player.market_value) <= self.market_value[1]
            ):
                age = player.age
                if age not in age_rating_data:
                    age_rating_data[age] = 0
                    age_count[age] = 0

                age_rating_data[age] += player.average_rating
                age_count[age] += 1

        return [
            {
                "age": age,
                "average rating": round(
                    age_rating_data.get(age, 0) / age_count.get(age, 1), 2
                ),
            }
            for age in range(self.age[0], self.age[1] + 1)  # Ensure we include all ages
        ]

    def add_selected(self, list_name: str, item: str):
        self.selected_items[list_name].append(item)

    def remove_selected(self, list_name: str, item: str):
        self.selected_items[list_name].remove(item)

    def add_all_selected(self, list_name: str):
        self.selected_items[list_name] = list(all_items[list_name])

    def clear_selected(self, list_name: str):
        self.selected_items[list_name].clear()

    def random_selected(self, list_name: str):
        self.selected_items[list_name] = np.random.choice(
            all_items[list_name],
            size=np.random.randint(1, len(all_items[list_name]) + 1),
            replace=False,
        ).tolist()


    @rx.event
    def handle_submit_game_data(self, form_data: dict):
        import datetime

        self.form_data = form_data
        db_connection_string = 'postgresql://postgres:asgard123@localhost/football'

        def connect_to_db(db_connection_string):
            try:
                engine = create_engine(db_connection_string)
                print("Connection to the database was successful!")
                return engine
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                return None

        engine = connect_to_db(db_connection_string)
        if not engine:
            return rx.window_alert("Error connecting to the database")

        connection = engine.connect()

        try:
            # Extract game-related input
            home_club_name = form_data['home_club']
            home_club_goals = int(form_data["home_goals"])
            away_club_name = form_data["away_club"]
            away_club_goals = int(form_data["away_goals"])
            game_date = datetime.datetime.strptime(form_data["date"], "%Y-%m-%d").date()
            competition_name = form_data["competition_name"]
            competition_round = form_data["round_name"]

            # Determine the season
            season_query = text("""
                SELECT season_id
                FROM seasons
                WHERE season_start_date <= :game_date AND season_end_date >= :game_date
            """)
            season = connection.execute(season_query, {"game_date": game_date}).fetchone()
            if not season:
                return rx.window_alert("No season found for the given date")
            season_id = season.season_id

            # Find competition ID
            competition_query = text("""
                SELECT competition_id
                FROM competitions
                WHERE name = :competition_name
            """)
            competition = connection.execute(competition_query, {"competition_name": competition_name}).fetchone()
            if not competition:
                return rx.window_alert("Competition not found")
            competition_id = competition.competition_id

            round_query = text("""
                SELECT cr_id
                FROM competition_rounds
                WHERE round_name = :round_name AND competition_id = :competition_id
            """)
            cr = connection.execute(round_query, {"round_name": competition_round, "competition_id": competition_id}).fetchone()
            if not cr:
                insert_round_query = text("""
                    INSERT INTO competition_rounds (round_name, competition_id)
                    VALUES (:round_name, :competition_id)
                    RETURNING cr_id
                """)
                cr_id = connection.execute(insert_round_query, {"round_name": competition_round, "competition_id": competition_id}).fetchone().cr_id
            else:
                cr_id = cr.cr_id

            club_query = text("""
                SELECT club_id
                FROM clubs
                WHERE name = :club_name
            """)
            home_club = connection.execute(club_query, {"club_name": home_club_name}).fetchone()
            away_club = connection.execute(club_query, {"club_name": away_club_name}).fetchone()
            if not home_club or not away_club:
                return rx.window_alert("One or both clubs not found")
            home_club_id = home_club.club_id
            away_club_id = away_club.club_id

            if home_club_goals > away_club_goals:
                winner_club_id = home_club_id
            elif home_club_goals < away_club_goals:
                winner_club_id = away_club_id
            else:
                winner_club_id = None  # Draw

            random_game_id = random.randint(400000, 999999)

            game_query = text("""
                INSERT INTO games (game_id, season_id, date, home_club_id, away_club_id, 
                                home_club_goals, away_club_goals, winner_club_id, cr_id)
                VALUES (:game_id, :season_id, :game_date, :home_club_id, :away_club_id,
                        :home_club_goals, :away_club_goals, :winner_club_id, :cr_id)
            """)
            game_data = {
                "game_id": random_game_id,
                "season_id": season_id,
                "game_date": game_date,
                "home_club_id": home_club_id,
                "away_club_id": away_club_id,
                "home_club_goals": home_club_goals,
                "away_club_goals": away_club_goals,
                "winner_club_id": winner_club_id,
                "cr_id": cr_id
            }
            connection.execute(game_query, game_data)

            connection.commit()
            print("Game data inserted successfully!")
            State.load_entries()
            yield rx.toast("Game data saved!")

        except Exception as e:
            connection.rollback()
            print(f"An error occurred: {e}")
            return rx.window_alert("Error while inserting game data into the database")


        finally:
            connection.close()


    
    @rx.event
    def handle_submit_player_performance(self, form_data: dict):
        db_connection_string = 'postgresql://postgres:asgard123@localhost/football'
        
        def connect_to_db(db_connection_string):
            try:
                engine = create_engine(db_connection_string)
                print("Connection to the database was successful!")
                return engine
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                return None

        # Connect to the database
        engine = connect_to_db(db_connection_string)
        if not engine:
            rx.window_alert("Error connecting to the database")
            return None

        connection = engine.connect()

        try:
            # Extract form data
            game_date = datetime.strptime(form_data["date"], "%Y-%m-%d").date()
            home_club_name = form_data["home_club"]
            away_club_name = form_data["away_club"]
            player_name = form_data["player_name"]
            goals = int(form_data["player_goals"])
            assists = int(form_data["player_assists"])
            rating = float(form_data["player_rating"])

            # Check if there was a game on the given date between the two clubs
            game_query = text("""
                SELECT game_id
                FROM games
                WHERE date = :game_date
                AND home_club_id = (SELECT club_id FROM clubs WHERE name = :home_club_name)
                AND away_club_id = (SELECT club_id FROM clubs WHERE name = :away_club_name)
            """)
            game_result = connection.execute(game_query, {"game_date": game_date, "home_club_name": home_club_name, "away_club_name": away_club_name}).fetchone()

            if not game_result:
                return rx.window_alert("No game found for the specified clubs on the given date.")

            game_id = game_result.game_id

            player_query = text("""
                SELECT player_id, current_club_id
                FROM players
                WHERE name = :player_name
            """)
            player_result = connection.execute(player_query, {"player_name": player_name}).fetchone()

            if not player_result:
               return rx.window_alert("Player not found.")
            
            player_id = player_result.player_id
            current_club_id = player_result.current_club_id

            home_club_id = connection.execute(text("""
                SELECT club_id FROM clubs WHERE name = :home_club_name
            """), {"home_club_name": home_club_name}).fetchone().club_id

            away_club_id = connection.execute(text("""
                SELECT club_id FROM clubs WHERE name = :away_club_name
            """), {"away_club_name": away_club_name}).fetchone().club_id

            if current_club_id not in [home_club_id, away_club_id]:
                return rx.window_alert(f"Player is not registered for either {home_club_name} or {away_club_name}.")

            season_query = text("""
                SELECT season_id
                FROM seasons
                WHERE season_start_date <= :game_date AND season_end_date >= :game_date
            """)
            season_result = connection.execute(season_query, {"game_date": game_date}).fetchone()
            if not season_result:
                return rx.window_alert("No season found for the given date.")
            
            season_id = season_result.season_id

            stats_query = text("""
                INSERT INTO player_statistics (player_id, game_id, season_id, goals, assists, yellow_cards, red_cards, minutes_played, rating)
                VALUES (:player_id, :game_id, :season_id, :goals, :assists, :yellow_cards, :red_cards, :minutes_played, :rating)
            """)
            stats_data = {
                "player_id": player_id,
                "game_id": game_id,
                "season_id": season_id,
                "goals": goals,
                "assists": assists,
                "yellow_cards": 0,  
                "red_cards": 0,     
                "minutes_played": 90,  
                "rating": rating
            }
            connection.execute(stats_query, stats_data)

            connection.commit()
            print("Player performance data inserted successfully!")
            State.load_entries()
            yield rx.toast("Player performance data saved!")

        except Exception as e:
            connection.rollback()
            print(f"An error occurred: {e}")
            return rx.window_alert("Error while inserting player performance data into the database.")

        finally:
            connection.close()



    @rx.event
    def handle_update_player_transfer(self, form_data: dict):
        
        player_name = form_data['player_name']
        club_name = form_data['club_name']
        transfer_value = float(form_data['transfer_value'])

        db_connection_string = 'postgresql://postgres:asgard123@localhost/football'

        def connect_to_db(db_connection_string):
            try:
                engine = create_engine(db_connection_string)
                return engine
            except SQLAlchemyError as e:
                return None

        engine = connect_to_db(db_connection_string)
        if not engine:
            return rx.window_alert("Error connecting to the database")

        connection = engine.connect()

        try:
            player_query = text("""
                SELECT player_id, current_club_id
                FROM players
                WHERE name = :player_name
            """)
            player = connection.execute(player_query, {"player_name": player_name}).fetchone()
            if not player:
                return rx.window_alert(f"Player {player_name} not found")

            player_id = player.player_id
            current_club_id = player.current_club_id

            club_query = text("""
                SELECT club_id
                FROM clubs
                WHERE name = :club_name
            """)
            club = connection.execute(club_query, {"club_name": club_name}).fetchone()
            if not club:
                return rx.window_alert(f"Club {club_name} not found")

            new_club_id = club.club_id

            if current_club_id == new_club_id:
                return rx.window_alert(f"Player {player_name} is already at {club_name}")

            if transfer_value < 0:
                return rx.window_alert("Transfer value cannot be negative")

            update_player_query = text("""
                UPDATE players
                SET current_club_id = :new_club_id
                WHERE player_id = :player_id
            """)
            connection.execute(update_player_query, {"new_club_id": new_club_id, "player_id": player_id})

            update_valuation_query = text("""
                INSERT INTO player_valuations (player_id, date, market_value_in_eur)
                VALUES (:player_id, CURRENT_DATE, :transfer_value)
            """)
            connection.execute(update_valuation_query, {"player_id": player_id, "transfer_value": transfer_value})

            connection.commit()
            print(f"Player {player_name} transferred to {club_name} with value {transfer_value} EUR.")
            State.load_entries()  
            yield rx.toast("Player transfer updated successfully!")

        except SQLAlchemyError as e:
            connection.rollback()
            print(f"An error occurred: {e}")
            return rx.window_alert("Error while updating the player transfer")

        finally:
            connection.close()


    @rx.event
    def generate_game_stats_json(self, form_data: dict):
        try:
            year_str = form_data.get("year", "").strip()
            if not year_str.isdigit():
                return rx.window_alert("Error: Year must be a numeric value.")

            year = int(year_str)

            if not (2021 <= year <= 2024):
                return rx.window_alert("Error: Year must be between 2021 and 2024.")

            db_connection_string = "postgresql://postgres:asgard123@localhost/football"

            engine = create_engine(db_connection_string)
            connection = engine.raw_connection()  
            cursor = connection.cursor()
            
            rx.toast("Forming your file, it may take a few minutes")

            games_query = """
                SELECT g.game_id, g.date, g.home_club_goals, g.away_club_goals,
                    g.home_club_id, g.away_club_id, hc.name AS home_club_name, 
                    ac.name AS away_club_name, g.cr_id, c.name AS competition_name, 
                    cr.round_name,
                    p.name AS player_name, 
                    DATE_PART('year', AGE(p.date_of_birth)) AS age,
                    cn.country_name AS nationality,
                    p.market_value_in_eur AS market_value,
                    ps.goals AS goals, 
                    ps.assists AS assists, 
                    ps.rating AS rating
                FROM games g
                JOIN competition_rounds cr ON g.cr_id = cr.cr_id
                JOIN competitions c ON cr.competition_id = c.competition_id
                JOIN clubs hc ON g.home_club_id = hc.club_id
                JOIN clubs ac ON g.away_club_id = ac.club_id
                LEFT JOIN player_statistics ps ON g.game_id = ps.game_id
                LEFT JOIN players p ON ps.player_id = p.player_id
                LEFT JOIN countries cn ON p.nationality_id = cn.country_id
                WHERE EXTRACT(YEAR FROM g.date) = %s
                ORDER BY g.game_id, ps.player_id;
            """
            cursor.execute(games_query, (year,))

            games = {}
            for row in cursor.fetchall():
                game_id = row[0]

                if game_id not in games:
                    games[game_id] = {
                        "date": row[1].strftime("%Y-%m-%d"),
                        "home_club_goals": row[2],
                        "away_club_goals": row[3],
                        "home_club_name": row[6],
                        "away_club_name": row[7],
                        "competition": {
                            "name": row[9],
                            "round_name": row[10],
                        },
                        "players": [],
                    }

                if row[11]:  # Check if player data exists
                    games[game_id]["players"].append({
                        "name": row[11],
                        "age": int(row[12]) if row[12] else None,
                        "nationality": row[13],
                        "market_value": float(row[14]) if row[14] else None,
                        "stats": {
                            "goals": int(row[15]) if row[15] is not None else 0,
                            "assists": int(row[16]) if row[16] is not None else 0,
                            "rating": float(row[17]) if row[17] else None,
                        }
                    })

            # Convert games dictionary to a list for JSON output
            all_games = list(games.values())

            # Generate JSON data
            json_data = json.dumps(all_games, indent=4)

            # Set the filename
            file_name = f"games_stats_{year}.json"

            #print(f"Data to download: {json_data}")
            return rx.download(data=json_data, filename=file_name)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return rx.window_alert(f"An error occurred: {str(e)}")

        finally:
            # Close the cursor and connection
            if "cursor" in locals() and cursor:
                cursor.close()
            if "connection" in locals() and connection:
                connection.close()






    @rx.event
    def fill_oltp(self):
        self.fill_oltp()
        return rx.window_alert("Loaded!")


    def connect_to_db(self, db_connection_string):
        try:
            engine = create_engine(db_connection_string)
            connection = engine.connect()
            print("Підключення до бази даних успішне!")
            return engine
        except OperationalError as e:
            print(f"Помилка підключення до бази даних: {e}")
            return None
        

    def load_unique_countries(self, csv_file_path, engine):
        if engine is not None:
            players = pd.read_csv(csv_file_path)
            
            # Вибір унікальних записів з колонки country_of_citizenship
            unique_countries = players['country_of_citizenship'].dropna().unique()
            
            # Створення DataFrame для завантаження в базу даних
            countries_df = pd.DataFrame({
                'country_id': [0] + list(range(1, len(unique_countries) + 1)),
                'country_name': ['Other'] + list(unique_countries)
            })
            
            # Завантаження даних у таблицю countries
            countries_df.to_sql('countries', engine, if_exists='append', index=False)
            
            print("Дані про країни успішно завантажені в базу даних.")
        else:
            print("Не вдалося підключитися до бази даних. Дані не завантажено.")

    def load_competitions(self, competitions_csv_path, engine):
        
        # Завантаження даних з CSV файлу
        competitions_df = pd.read_csv(competitions_csv_path)
        
        # Вибір необхідних колонок
        competitions_df = competitions_df[['competition_id', 'name', 'type', 'country_name']]
        
        # Завантаження таблиці countries з бази даних
        countries_df = pd.read_sql('SELECT country_id, country_name FROM countries', engine)
        
        # Злиття (merge) даних для отримання country_id
        merged_df = competitions_df.merge(countries_df, left_on='country_name', right_on='country_name', how='left')
        
        # Замінюємо відсутні country_id на 0
        merged_df['country_id'] = merged_df['country_id'].fillna(0)
        
        # Перетворення типу даних для country_id
        merged_df['country_id'] = merged_df['country_id'].astype(int)
        
        # Відбір необхідних колонок для завантаження в таблицю competitions
        final_competitions_df = merged_df[['competition_id', 'name', 'type', 'country_id']]
        
        # Завантаження даних у таблицю competitions
        final_competitions_df.to_sql('competitions', engine, if_exists='append', index=False)
        
        print("Дані про змагання успішно завантажені в базу даних.")

    def load_seasons(self, engine):
        # Створення списків з потрібними датами
        season_start_dates = pd.date_range(start="2021-08-01", end="2024-08-01", freq='YS-AUG')
        season_end_dates = pd.date_range(start="2022-07-31", end="2025-07-31", freq='YE-JUL')
        
        # Формування списків для ключа як рік початку сезону
        season_keys = [start.year for start in season_start_dates]
        
        # Створення DataFrame
        seasons_df = pd.DataFrame({
            'season_id': season_keys,
            'season_start_date': season_start_dates,
            'season_end_date': season_end_dates
        })
        
        # Завантаження даних у таблицю seasons
        seasons_df.to_sql('seasons', engine, if_exists='append', index=False)
        
        print("Дані про сезони успішно завантажені в базу даних.")

    def load_clubs(self, csv_file_path, engine):
        # Завантаження даних з CSV файлу
        clubs_df = pd.read_csv(csv_file_path)
        
        # Вибір необхідних колонок
        clubs_df = clubs_df[['club_id', 'name', 'domestic_competition_id', 'last_season']]
        
        # Відкидання клубів, де last_season менше 2024
        clubs_df = clubs_df[clubs_df['last_season'] >= 2021]
        
        # Вибір колонок для завантаження в таблицю clubs
        final_clubs_df = clubs_df[['club_id', 'name', 'domestic_competition_id']]
        
        # Завантаження даних у таблицю clubs
        final_clubs_df.to_sql('clubs', engine, if_exists='append', index=False)
        
        print("Дані про клуби успішно завантажені в базу даних.")

    def load_positions(self, csv_file_path, engine):
        # Завантаження даних з CSV файлу
        players_df = pd.read_csv(csv_file_path)
        
        # Вибір необхідних колонок
        positions_df = players_df[['position', 'sub_position']].drop_duplicates().dropna()
        
        # Додавання стовпця position_id
        positions_df.reset_index(drop=True, inplace=True)
        positions_df['position_id'] = positions_df.index + 1
        
        # Перестановка колонок для відповідності структурі таблиці positions
        positions_df = positions_df[['position_id', 'position', 'sub_position']]
        
        # Перейменування колонок для відповідності структурі таблиці positions
        positions_df.columns = ['position_id', 'position_name', 'sub_position_name']
        
        # Завантаження даних у таблицю positions
        positions_df.to_sql('positions', engine, if_exists='append', index=False)
        
        print("Дані про позиції успішно завантажені в базу даних.")

    def load_players(self, players_csv_path, engine):
        # Завантаження даних з CSV файлу
        players_df = pd.read_csv(players_csv_path)
        
        # Вибір необхідних колонок
        players_df = players_df[['player_id', 'name', 'date_of_birth', 'foot', 'height_in_cm',
                                'country_of_citizenship', 'last_season', 'position', 'sub_position',
                                'current_club_id', 'market_value_in_eur']]
        
        # Відкидання гравців, де last_season менше 2024
        players_df = players_df[players_df['last_season'] >= 2024]
        
        # Завантаження таблиці countries з бази даних
        countries_df = pd.read_sql('SELECT country_id, country_name FROM countries', engine)
        
        # Завантаження таблиці positions з бази даних
        positions_df = pd.read_sql('SELECT position_id, position_name, sub_position_name FROM positions', engine)
        
        # Злиття (merge) даних для отримання country_id
        merged_df = players_df.merge(countries_df, left_on='country_of_citizenship', right_on='country_name', how='left')
        
        # Злиття (merge) даних для отримання position_id
        merged_df = merged_df.merge(positions_df, left_on=['position', 'sub_position'], right_on=['position_name', 'sub_position_name'], how='left')
        
        # Замінюємо відсутні country_id на 0
        merged_df['country_id'] = merged_df['country_id'].fillna(0).astype(int)
        
        # Відбір необхідних колонок для завантаження в таблицю players
        final_players_df = merged_df[['player_id', 'name', 'date_of_birth', 'foot', 'height_in_cm', 'country_id',
                                    'current_club_id', 'market_value_in_eur', 'position_id']]
        
        # Перейменування колонок для відповідності структурі таблиці players
        final_players_df.columns = ['player_id', 'name', 'date_of_birth', 'foot', 'height_in_cm', 'nationality_id',
                                    'current_club_id', 'market_value_in_eur', 'position_id']
        
        # Завантаження даних у таблицю players
        final_players_df.to_sql('players', engine, if_exists='append', index=False)
        
        print("Дані про гравців успішно завантажені в базу даних.")

        

    def load_player_valuations(self, valuations_file, engine):
        # Завантажуємо дані з таблиці `players` для перевірки наявності player_id
        players = pd.read_sql_table('players', con=engine, columns=['player_id'])
        
        # Зчитуємо дані з файлу player_valuations.csv
        valuations = pd.read_csv(valuations_file, usecols=['player_id', 'date', 'market_value_in_eur'])
        
        # Фільтруємо дати, залишаючи лише записи з 2021 року або новіші
        cutoff_date = datetime(2021, 1, 1)
        valuations['date'] = pd.to_datetime(valuations['date'])
        valuations = valuations[valuations['date'] >= cutoff_date]
        
        # Перевіряємо наявність player_id в таблиці `players`, відкидаємо зайві записи
        valid_players = set(players['player_id'])
        valuations = valuations[valuations['player_id'].isin(valid_players)]
        
        # Завантажуємо дані в таблицю player_valuations
        valuations.to_sql('player_valuations', con=engine, if_exists='append', index=False)
        print("Дані про вартість успішно завантажені в базу даних.")


    def load_competition_rounds(self, games_csv_path, engine):
        # Завантаження даних з CSV файлу
        games_df = pd.read_csv(games_csv_path)
        
        # Вибір необхідних колонок
        rounds_df = games_df[['competition_id', 'round']].drop_duplicates().dropna()
        
        # Додавання стовпця cr_id з унікальними значеннями
        rounds_df.reset_index(drop=True, inplace=True)
        rounds_df['cr_id'] = rounds_df.index + 1
        
        # Перестановка колонок для відповідності структурі таблиці competition_rounds
        rounds_df = rounds_df[['cr_id', 'competition_id', 'round']]
        
        # Перейменування колонок для відповідності структурі таблиці competition_rounds
        rounds_df.columns = ['cr_id', 'competition_id', 'round_name']
        
        # Завантаження даних у таблицю competition_rounds
        rounds_df.to_sql('competition_rounds', engine, if_exists='append', index=False)
        
        print("Дані про раунди змагань успішно завантажені в базу даних.")



    def load_games(self, games_csv_path, engine):
        # Завантаження даних з CSV файлу
        games_df = pd.read_csv(games_csv_path)
        
        # Вибір необхідних колонок
        games_df = games_df[['game_id', 'season', 'date', 
                            'home_club_id', 'away_club_id', 
                            'home_club_goals', 'away_club_goals', 
                            'winner_club_id', 'round']]
        
        # Відкидання ігор, сезон яких менший за 2021
        games_df = games_df[games_df['season'] >= 2021]
        
        # Завантаження таблиці clubs з бази даних
        clubs_df = pd.read_sql('SELECT club_id FROM clubs', engine)
        
        # Перетворення стовпця club_id на набір для швидкої перевірки
        valid_club_ids = set(clubs_df['club_id'])
        
        # Відкидання ігор, де home_club_id або away_club_id не в списку club_id
        games_df = games_df[games_df['home_club_id'].isin(valid_club_ids) & games_df['away_club_id'].isin(valid_club_ids)]
        
        # Завантаження таблиці competition_rounds з бази даних
        competition_rounds_df = pd.read_sql('SELECT cr_id, round_name FROM competition_rounds', engine)
        
        # Відповідність значень 'round' зі значеннями 'cr_id'
        round_to_cr_id = dict(zip(competition_rounds_df['round_name'], competition_rounds_df['cr_id']))
        
        # Додавання стовпця cr_id на основі round
        games_df['cr_id'] = games_df['round'].map(round_to_cr_id)
        
        # Відкидання ігор, для яких cr_id не знайдено
        games_df = games_df.dropna(subset=['cr_id'])
        
        # Перетворення cr_id до типу int
        games_df['cr_id'] = games_df['cr_id'].astype(int)
        
        # Перейменування колонки 'season' на 'season_id'
        games_df = games_df.rename(columns={'season': 'season_id'})
        
        # Видалення зайвої колонки 'round'
        games_df = games_df.drop(columns=['round'])
        
        # Завантаження даних у таблицю games
        games_df.to_sql('games', engine, if_exists='append', index=False)
        
        print("Дані про ігри успішно завантажені в базу даних.")


    def load_player_statistics(self, appearances_file, engine):
        # Завантажуємо дані з таблиць `players` і `games` для перевірки наявності player_id та game_id
        players = pd.read_sql_table('players', con=engine, columns=['player_id'])
        games = pd.read_sql_table('games', con=engine, columns=['game_id'])
        
        # Зчитуємо дані з файлу appearances.csv
        appearances = pd.read_csv(appearances_file, usecols=[
            'game_id', 'player_id', 'player_club_id', 'date', 
            'yellow_cards', 'red_cards', 'goals', 'assists', 'minutes_played', 'rating'
        ])
        
        # Фільтруємо дати, залишаючи лише записи з 1 серпня 2021 року або новіші
        cutoff_date = datetime(2021, 8, 1)
        appearances['date'] = pd.to_datetime(appearances['date'])
        appearances = appearances[appearances['date'] >= cutoff_date]
        
        # Перевіряємо наявність player_id та game_id в базі даних, відкидаємо зайві записи
        valid_players = set(players['player_id'])
        valid_games = set(games['game_id'])
        appearances = appearances[
            appearances['player_id'].isin(valid_players) & 
            appearances['game_id'].isin(valid_games)
        ]
        
        # Додаємо колонку season_id на основі дати
        def calculate_season_id(date):
            year = date.year
            # Якщо місяць від серпня до грудня, використовуємо поточний рік, інакше - попередній
            return year if date.month >= 8 else year - 1
        
        appearances['season_id'] = appearances['date'].apply(calculate_season_id)
        
        # Вибираємо необхідні колонки для таблиці player_statistics
        player_statistics = appearances[[
            'player_id', 'game_id', 'season_id', 
            'goals', 'assists', 'yellow_cards', 'red_cards', 'minutes_played', 'rating'
        ]]
        
        # Завантажуємо дані в таблицю player_statistics
        player_statistics.to_sql('player_statistics', con=engine, if_exists='append', index=False)
        print("Дані про статистику успішно завантажені в базу даних.")

    def truncate_tables(self, connection_string):
        try:
            # Establish a connection
            with psycopg2.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    # Disable foreign key constraints
                    cursor.execute("SET session_replication_role = 'replica';")
                    print("Foreign key constraints disabled.")

                    # List of tables to truncate
                    tables = [
                        "player_statistics",
                        "player_valuations",
                        "games",
                        "players",
                        "clubs",
                        "positions",
                        "competition_rounds",
                        "competitions",
                        "seasons",
                        "countries",
                    ]

                    # Truncate each table with CASCADE
                    for table in tables:
                        cursor.execute(SQL("TRUNCATE TABLE {} CASCADE;").format(Identifier(table)))
                        print(f"Truncated table: {table}")

                    # Re-enable foreign key constraints
                    cursor.execute("SET session_replication_role = 'origin';")
                    print("Foreign key constraints re-enabled.")

                # Commit the transaction
                conn.commit()
                print("Truncation completed successfully.")

        except psycopg2.Error as e:
            print(f"An error occurred while truncating tables: {e}")

    competitions_csv_path = 'D:/data/football/competitions.csv'
    countries_csv_path = 'D:/data/football/players.csv'
    player_valuations_csv_path = 'D:/data/football/player_valuations.csv'
    games_csv_path = 'D:/data/football/games.csv'
    clubs_csv_path = 'D:/data/football/clubs.csv'
    appearances_csv_path = 'D:/data/football/appearances.csv'
    players_csv_path = 'D:/data/football/players.csv'
    db_connection_string = 'postgresql://postgres:asgard123@localhost/football'

    def fill_oltp(self):

        engine = self.connect_to_db(self.db_connection_string)

        self.truncate_tables(self.db_connection_string)

        self.load_unique_countries(self.countries_csv_path, engine)
        self.load_competitions(self.competitions_csv_path, engine)
        self.load_seasons(engine)
        self.load_clubs(self.clubs_csv_path, engine)
        self.load_positions(self.players_csv_path, engine)
        self.load_players(self.players_csv_path, engine)
        self.load_player_valuations(self.player_valuations_csv_path, engine)
        self.load_competition_rounds(self.games_csv_path, engine)
        self.load_games(self.games_csv_path, engine)
        self.load_player_statistics(self.appearances_csv_path, engine)




