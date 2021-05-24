from django.db import models
from pytz import unicode


class Directory(models.Model):
    name_of_directory = models.CharField(max_length=200, verbose_name="Имя папки")

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'

    def __str__(self):
        return unicode(str(self.name_of_directory))

def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/name_dir/<filename>
    return '{0}/{1}'.format(instance.directory.name_of_directory, filename)

class File(models.Model):
    TYPE_OF_FILES = (('work', 'Схема производства работ'),
                     ('exploitation', 'Схема на период эксплуатации'),
                     ('tome', 'Том'))

    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, verbose_name="Имя папки")
    file = models.FileField(upload_to=directory_path, verbose_name="Файл")
    format_of_file = models.CharField(max_length=50, choices=TYPE_OF_FILES, verbose_name="Формат файла")

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return unicode(str(self.file))

class TelegramUser(models.Model):
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=100, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    isAdmin = models.BooleanField(verbose_name='Админ', default=False)
    enable_directory = models.ForeignKey(Directory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Имя папки")
    code_for_verification = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пользователь телеграм'
        verbose_name_plural = 'Пользователи телеграм'
