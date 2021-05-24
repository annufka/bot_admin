from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("verificate", "Верификация"),
        types.BotCommand("find", "Поиск файла"),
        types.BotCommand("add_user", "Добавить пользователя (только для админа)"),
        types.BotCommand("add_file", "Добавить файл (только для админа)"),
        types.BotCommand("add_dir", "Добавить папку (только для админа)"),
        types.BotCommand("cancel", "Отмена начала создания папки, пользователя, файла (только для админа)"),
    ])
