from django.apps import AppConfig


class RegularMessageConfig(AppConfig):
    name = 'scheduler'

    
    def ready(self):
        '''Start a scheduler when the app starts.'''

        from scheduler import scheduler
        scheduler.start()
