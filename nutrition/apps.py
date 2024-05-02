from django.apps import AppConfig

class NutritionConfig(AppConfig):
    name = 'nutrition'

    def ready(self):
        import nutrition.signals
