from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import watch_callback

get_marks_keyboard = ReplyKeyboardMarkup(
    row_width=4,
    keyboard=[
        [
            KeyboardButton(text = "Годовые Оценки", callback_data='marks_for_year')
        ],
        [
            KeyboardButton(text = "Итоговые оценки", callback_data='period_final_marks')
        ],
        [
            KeyboardButton(text = "Текущие оценки за все предметы", callback_data='current_marks_for_all_subjects')
        ],
        [
            KeyboardButton(text = "Текущие оценки за один предмет.\n Выберите предмет ...", callback_data="current_marks_for_one_subject")
        ],
        [
            KeyboardButton(text = 'Оценки за экзамены ОГЭ/ЕГЭ', callback_data = ' exam_marks')
        ],
    ]
)