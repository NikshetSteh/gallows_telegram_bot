import user
import config

from mysql.connector import connect, Error
import logging

class Loader:
    @staticmethod
    def load(users: dict):
        logging.info("load data...")

        with connect(host = config.DATABESE_HOST, user = config.DATABESE_USER, password = config.DATABESE_PASSWORD, database = "epiz_31926153_top_secret") as database:
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

        with connect(host = config.DATABESE_HOST, user = config.DATABESE_USER, password = config.DATABESE_PASSWORD, database = "epiz_31926153_top_secret") as database:
            cursor = database.cursor()

            query = """ INSERT INTO users(id, games, wins, points) VALUES(?, ?, ?, ?); """
            query_for_delete = """ DELETE FROM users; """

            cursor.execute(query_for_delete)
            cursor.executemany(query, data)

            database.commit()

        logging.info("save data successful...")