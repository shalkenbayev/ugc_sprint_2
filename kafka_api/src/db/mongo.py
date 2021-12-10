from pymongo import MongoClient
from pymongo.database import Database

from core.config import Settings
from models.events import UserLike, UserSaveFilms, UserComment


class Mongo:

    def __init__(self):
        self.client: MongoClient = MongoClient(host=Settings.mongo_host, port=27017)

    def save_data_like(self, data: UserLike):
        like_db: Database = self.client.like_db
        like_db.test_data.insert_one(data.dict())

    def save_data_save_film(self, data: UserSaveFilms):
        user_save_film: Database = self.client.save_film
        user_save_film.test_data.insert_one(data.dict())

    def save_data_save_comment(self, data: UserComment):
        user_comment: Database = self.client.user_comment
        user_comment.test_data.insert_one(data.dict())
