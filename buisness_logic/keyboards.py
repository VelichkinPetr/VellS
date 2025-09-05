from typing import Any
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from buisness_logic.states import TestState


def create_keyboard(elements: list[Any], callback: str):
    inl_kb_builder = InlineKeyboardBuilder()
    if type(elements[0]).__name__ == 'Tests':
        for elem in elements:
            inl_btn = InlineKeyboardButton(text=str(elem.number),
                                                  callback_data=f"{type(elements[0]).__name__} {elem.id}")
            inl_kb_builder.add(inl_btn)
    else:
        for elem in elements:
            inl_btn = InlineKeyboardButton(text=elem.name, callback_data=f"{type(elements[0]).__name__} {elem.id}")
            inl_kb_builder.add(inl_btn)

    if type(elements[0]).__name__ != 'Subjects':
        inl_btn_back = InlineKeyboardButton(text='<<< Назад',
                                              callback_data = callback)
        inl_kb_builder.add(inl_btn_back)

    return inl_kb_builder.as_markup(resize_keyboard=True)