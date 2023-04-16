from django.db import models
from accounts.models import CustomUser

class Position(models.Model):
    position_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('position_name',)
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.position_name


class Level(models.Model):
    level_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('level_name',)
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'

    def __str__(self):
        return self.level_name


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name
    

class Localization(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)

    class Meta:
        ordering = ('city',)
        verbose_name = 'Localization'
        verbose_name_plural = 'Localizations'

    def __str__(self):
        return self.city



class Contract(models.Model):
    contract_type = models.CharField(max_length=50)

    class Meta:
        ordering = ('contract_type',)
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
    

    def __str__(self):
        return self.contract_type


class Offer(models.Model):
    name = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    contract = models.ManyToManyField(Contract)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    remote = models.BooleanField(default=False)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def salary(self):
        if self.salary_from is None and self.salary_to is None:
            return "Niezdefiniowana"
        elif self.salary_from is None:
            return f"do {self.salary_to}"
        elif self.salary_to is None:
            return f"od {self.salary_from}"
        else:
            return f"{self.salary_from} - {self.salary_to}"
        
    class Meta:
        ordering = ('name',)
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
    

    def __str__(self):
        return self.name
