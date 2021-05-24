from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(inline_keyboard=
[
    [InlineKeyboardButton(text="Схема производства работ", callback_data="find#work"), ],

    [InlineKeyboardButton(text="Схема на период эксплуатации", callback_data="find#explotation"), ],

    [InlineKeyboardButton(text="Том", callback_data="find#tome"), ]
]
)


choice_for_create = InlineKeyboardMarkup(inline_keyboard=
[
    [InlineKeyboardButton(text="Схема производства работ", callback_data="createcategory#work"), ],

    [InlineKeyboardButton(text="Схема на период эксплуатации", callback_data="createcategory#explotation"), ],

    [InlineKeyboardButton(text="Том", callback_data="createcategory#tome"), ]
]
)
