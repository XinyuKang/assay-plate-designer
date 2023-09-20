from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

# Create your models here.


class Plate(models.Model):
    # Define a plate
    name = models.CharField(max_length=100)

class Well(models.Model):
    # Define a well
    # row and column coordinates
    row = models.IntegerField() 
    col = models.IntegerField()
    # fields for reagent, antibody, and concentration
    reagent = models.CharField(
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^R\d+$',
                message="Reagent must start with 'R' and followed by numbers.",
            ),
        ],
    )
    antibody = models.CharField(
        validators=[
            MinLengthValidator(limit_value=20, message="Amino acids sequence must be at least 20 characters long."),
            MaxLengthValidator(limit_value=40, message="Amino acids sequence cannot exceed 40 characters."),
        ],
        blank=True
    )
    concentration = models.FloatField(null=True, blank=True)
    # Establish relationship with Plate model
    # When Plate is deleted, all repated Well objects should also be automatically deleted
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE)