from django.apps import AppConfig


class BbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb'

    def ready(self):
        #включаем файл с обработчиком сигналов
        import bb.signals