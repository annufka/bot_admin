import os

from cabinet.models import File, Directory, TelegramUser
from asgiref.sync import sync_to_async


# выбрать пользователя
@sync_to_async
def select_user(email):
    return TelegramUser.objects.filter(email=email).first()


# добавить пользователя
@sync_to_async
def add_user(email):
    return TelegramUser(email=email).save()


# получить все папки из базы
def get_all_dir_from_db():
    return Directory.objects.all()


# добавить папку для доступа пользователя
@sync_to_async
def add_dir_to_user_in_db(email, name_dir):
    user = TelegramUser.objects.filter(email=email).first()
    user.enable_directory = Directory.objects.filter(name_of_directory=name_dir).first()
    user.save()
    return user


# все пользователи
def get_all_user():
    users = TelegramUser.objects.all()
    return users


# заполнение полей пользователя пользователем
@sync_to_async
def update_user_telegram_id(email, id):
    user = TelegramUser.objects.filter(email=email).first()
    user.telegram_id = id
    user.save()
    return user


# сменить код верификации в базе после генерации
@sync_to_async
def update_user_code(code, id):
    user = TelegramUser.objects.filter(telegram_id=id).first()
    user.code_for_verification = int(code)
    user.save()
    return user


# код верификации
@sync_to_async
def get_code(id):
    return TelegramUser.objects.filter(telegram_id=id).first().code_for_verification


# получить пользователя по ид
@sync_to_async
def get_user_by_id(id):
    try:
        return TelegramUser.objects.filter(telegram_id=id).first()
    except:
        return


@sync_to_async
def get_file(user_id, category, name):
    directory = TelegramUser.objects.filter(telegram_id=user_id).first().enable_directory
    file = File.objects.filter(directory_id=directory.id, format_of_file=category, file__contains=name).first()
    return str(file)


# все файлы с подходящей папки, названием и категорией
def get_files(user_id, category, name):
    directory = TelegramUser.objects.filter(telegram_id=user_id).first().enable_directory
    files = File.objects.filter(directory_id=directory.id, format_of_file=category, file__contains=name).values("file")
    return list(files)


# Список админов
@sync_to_async()
def get_all_admins():
    return list(TelegramUser.objects.filter(isAdmin=True).values("telegram_id"))


# добавить папку
@sync_to_async
def add_dir_to_db(name):
    return Directory(name_of_directory=name).save()


# добавить файл
@sync_to_async
def add_file_to_db(directory_name, file, category):
    directory = Directory.objects.filter(name_of_directory=directory_name).first()
    file_model = File(directory=directory, file=file, format_of_file="Схема производства работ").save()
    return file_model

