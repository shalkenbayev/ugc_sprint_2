from fastapi import APIRouter

from db.mongo import Mongo
from models.events import UserLike, UserSaveFilms, UserComment

user_event = APIRouter()
mongo = Mongo()


@user_event.post("/user_like")
async def user_like(data: UserLike):
    mongo.save_data_like(data)


@user_event.post("/user_save_film", response_model=UserSaveFilms)
async def user_save(data: UserSaveFilms):
    mongo.save_data_save_film(data)


@user_event.post("/user_comment", response_model=UserComment)
async def user_comment(data: UserComment):
    mongo.save_data_save_comment(data)
