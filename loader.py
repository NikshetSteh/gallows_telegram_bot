import user
import config

import sqlite3
import logging

class Loader:
    @staticmethod
    def load(users: dict):
        logging.info("load data...")

        with sqlite3.connect(config.DATABESE_PATH) as database:
            query = """ SELECT * FROM users """

            cursor = database.cursor()

            cursor.execute(query)

            for i in cursor:
                users.update({i[0]: user.User(i[0], games = i[1], wins = i[2], points = i[3])})

        logging.info(("load data successful"))

    @staticmethod
    def save(users: list):
        logging.info("save data...")

        if len(users) == 0:
            logging.info("hasnt data for save")
            return

        data = []

        for i in users:
            data.append((i.get_id(), i.get_games(), i.get_wins(), i.get_points()))

        with sqlite3.connect(config.DATABESE_PATH) as database:
            cursor = database.cursor()

            query = """ INSERT INTO users(id, games, wins, points) VALUES(?, ?, ?, ?); """
            query_for_delete = """ DELETE FROM users; """

            cursor.execute(query_for_delete)
            cursor.executemany(query, data)

            database.commit()

        logging.info("save data successful...")