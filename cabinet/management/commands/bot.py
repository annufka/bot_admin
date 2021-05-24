from django.core.management import BaseCommand


async def on_startup(dp):
    import telegram.filters
    import telegram.middlewares
    telegram.filters.setup(dp)
    telegram.middlewares.setup(dp)

    from telegram.utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from telegram.utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)


class Command(BaseCommand):
    help = "Телеграм бот"
    def handle(self, *args, **options):
        from aiogram import executor
        from telegram.handlers import dp

        executor.start_polling(dp, on_startup=on_startup)
