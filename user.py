import random

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from data import replicas
from enum import Enum
from random import randint

import logging

# TODO: achievement, leaders

QUESTION_MARK = "❓"
HEART_SYMBOL = "❤"

LIVES = 9

class Hard(Enum):
    easy = 1
    medium = 2
    hard = 3

hard_dict = {'Легко': Hard.easy.value, "Средне": Hard.medium.value, "Сложно": Hard.hard.value}

words_easy = []
words_medium = []
words_hard = []

words = {}


button_new_game = KeyboardButton('/новая_игра')
button_statistics = KeyboardButton('/статистика')
button_help_ = KeyboardButton('/помощь')
# button_leaders = KeyboardButton('/лидеры')


main_keybord = ReplyKeyboardMarkup(resize_keyboard=True)
main_keybord.insert(button_new_game).insert(button_statistics).insert(button_help_) # .insert(button_leaders)

def clear_str(src: str):
    return src.replace("\n", "")

def load_words(path):
    with open(path + "easy.data", encoding='UTF-8') as file:
        words_easy = list(map(clear_str, file.readlines()))
    with open(path + "medium.data", encoding='UTF-8') as file:
        words_medium = list(map(clear_str, file.readlines()))
    with open(path + "hard.data", encoding='UTF-8') as file:
        words_hard = list(map(clear_str, file.readlines()))

    words.update({Hard.easy.value: words_easy, Hard.medium.value: words_medium, Hard.hard.value: words_hard})


class Game:
    def __init__(self, lives, word):
        logging.info(f'creat new game {word} with {lives} lives')

        self.word = word
        self.lives = lives
        self.now_word = QUESTION_MARK * len(word)

    async def win(self, message: types.Message):
        await message.answer(replicas.REPLICAS_WIN.format(self.word), reply_markup = main_keybord)
        return True

    async def dead(self, message: types.Message):
        await message.answer(replicas.REPLICAS_DEAD.format(self.word), reply_markup = main_keybord)
        return False

    @staticmethod
    def __update_word(now_word, word, char):
        for i in range(len(word)):
            if word[i] == char:
                temp = list(now_word)
                temp[i] = char
                now_word = "".join(temp)

        if not QUESTION_MARK in now_word:
            return now_word, True
        else:
            return now_word, False

    async def open_symbol(self, message: types.Message):
        message_text = message.text.lower()

        if len(message_text) != 1:
            if message_text != self.word:
                self.lives -= 2

                if self.lives <= 0:
                    return await self.dead(message)

                await message.answer(replicas.REPLICAS_NO.format(self.now_word, HEART_SYMBOL * self.lives))

                return
            else:
                return await self.win(message)

        if message_text in self.now_word:
            await message.answer(replicas.REPLICAS_DOUBLE_CHAR)
            return

        if not message_text in self.word:
            self.lives -= 1

            if self.lives <= 0:
                return await self.dead(message)

            await message.answer(replicas.REPLICAS_NO.format(self.now_word, HEART_SYMBOL * self.lives))
        else:
            self.now_word, is_end = self.__update_word(self.now_word, self.word, message.text.lower())

            if is_end:
                return await self.win(message)
            else:
                await message.answer(replicas.REPLICAS_YES.format(self.now_word, HEART_SYMBOL * self.lives))

        return


class User:
    __id = 0
    __now_select_hard = False
    __hard = 0
    __games = 0
    __wins = 0
    __game = None
    __points = 0

    def __init__(self, id, games = 0, wins = 0, points = 0):
        self.__id = id
        self.__games = games
        self.__wins = wins
        self.__points = points

    async def __dont_understand(self, message: types.Message):
        await message.answer(replicas.REPLICAS_DONT_UNDERSTAND)

    async def print_statistics(self, message: types.Message):
        await message.answer(replicas.REPLICAS_STATISTICS.format(self.__games, self.__wins, self.__points))

    async def get_message(self, message: types.Message):
        if self.__now_select_hard:
            if not message.text in hard_dict:
                await self.__dont_understand(message)
                return

            self.__hard = hard_dict[message.text]

            self.is_game = True

            self.__game = Game(lives = 9, word = words[self.__hard][random.randint(0, len(words[self.__hard]) - 1)].lower())

            logging.info(f'player {self.__id} start game with __hard {self.__hard}')

            self.__games += 1

            await message.answer(replicas.REPLICAS_START_GAME.format(len(self.__game.word), LIVES), reply_markup = ReplyKeyboardRemove())
            self.__now_select_hard = False
            return

        if self.__game:
            buffer = await self.__game.open_symbol(message)

            if buffer:
                logging.info(f'player {self.__id} wins with word {self.__game.word}')
                self.__wins += 1
                self.__points += self.__hard

            if buffer != None:
                logging.info(f'player {self.__id} end game')
                self.__now_select_hard = False
                self.__hard = 0
                self.__game = None

            return

        await self.__dont_understand(message)

    async def start_game(self, message: types.Message):
        button_easy = KeyboardButton('Легко')
        button_medium = KeyboardButton('Средне')
        button_hard = KeyboardButton('Сложно')

        hard_selct_keybord = ReplyKeyboardMarkup(resize_keyboard = True)
        hard_selct_keybord.insert(button_easy).insert(button_medium).insert(button_hard)

        self.__now_select_hard = True

        await message.answer(replicas.REPLICAS_SELECT_HARD, reply_markup= hard_selct_keybord)

    def get_id(self):
        return self.__id

    def get_wins(self):
        return self.__wins

    def get_points(self):
        return self.__points

    def get_games(self):
        return self.__games