from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator  
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

from django.utils import timezone

class TrainingModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='trainings',null=True)
    date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.title
    
class SubTrainingModel(models.Model):
    training = models.ForeignKey(TrainingModel,on_delete=models.CASCADE,related_name='subtrainings')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='subtrainings')
    title = models.CharField(max_length=30)
    weight = models.CharField(max_length=10,default=0)
    set_number = models.PositiveIntegerField(blank=True,null=True,validators=[
       MaxValueValidator(99)])
    rep_number = models.PositiveIntegerField(blank=True,null=True,validators=[
        MaxValueValidator(999)])
    help_training = models.BooleanField(default=False)
    total_weight = models.FloatField(default=0.0,verbose_name="合計重量")

    def __str__(self):
        return self.title
    
    def calculate_total_weight(self):
        total_weight = int(self.weight) * int(self.set_number) * int(self.rep_number)
        total_weight = int(total_weight)
        return round(total_weight,2)
    
    def save(self,*args,**kwargs):
        self.total_weight = self.calculate_total_weight()
        super().save(*args,**kwargs)
    







class Auxiliary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    training = models.ForeignKey(TrainingModel,on_delete=models.CASCADE)
    subtraining = models.ForeignKey(SubTrainingModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','training','subtraining')










    
class MainTrainingModel(models.Model):
    training = models.ForeignKey(TrainingModel,on_delete=models.CASCADE,related_name='maintrainings')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='maintrainings')
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True)
    weight = models.CharField(max_length=10,default=0)
    set_number = models.PositiveIntegerField(blank=True,null=True,validators=[
        MaxValueValidator(99)])
    rep_number = models.PositiveIntegerField(blank=True,null=True,validators=[
        MaxValueValidator(999)])
    rm = models.PositiveIntegerField(blank=True,null=True,validators=[
        MaxValueValidator(99)])
    total_weight = models.FloatField(default=0.0,verbose_name="合計重量")

        
    def __str__(self):
        return self.title
    
    def calculate_total_weight(self):
        total_weight = int(self.weight) * int(self.set_number) * int(self.rep_number)
        total_weight = int(total_weight)
        return round(total_weight,2)
    
    def save(self,*args,**kwargs):
        self.total_weight = self.calculate_total_weight()
        super().save(*args,**kwargs)