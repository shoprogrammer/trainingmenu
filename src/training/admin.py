from django.contrib import admin
from .models import TrainingModel,SubTrainingModel,MainTrainingModel,Auxiliary

# Register your models here.
admin.site.register(TrainingModel)
admin.site.register(SubTrainingModel)
admin.site.register(MainTrainingModel)
admin.site.register(Auxiliary)