from django.db import models

class Plate(models.Model):
    TYPE = [
        ('384', '384'),
        ('96', '96')
    ]
    type = models.CharField(max_length=3, choices=TYPE, default='384')
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):    
        return self.name


class Well(models.Model):
    reagent = models.CharField(max_length=100, default="", blank=True)
    antibody = models.CharField(max_length=40, default="", blank=True)
    concentration = models.FloatField(default="0.0")
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE, default="", blank=True)
    row = models.IntegerField()
    col = models.IntegerField()

    def __str__(self):
        return self.reagent