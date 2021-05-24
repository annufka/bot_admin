from django.contrib import admin

from cabinet.models import Directory, File, TelegramUser

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
    # list_display = ['directory', 'file', 'format_of_file']

class FileInline(admin.StackedInline):
    model = File
    max_num = 1000
    extra = 0

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'telegram_id', 'user_name', 'isAdmin', 'enable_directory']

@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    # list_display = ['name_of_directory']
    inlines = [FileInline, ]
