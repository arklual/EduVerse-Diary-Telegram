# FSM

from aiogram.dispatcher.filters.state import StatesGroup, State

class SignInToDiary(StatesGroup):
    Locality = State()
    School = State()
    Login = State()
    Password = State()