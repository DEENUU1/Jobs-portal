from django.db import models
from accounts.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField


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


class Requirements(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Requirement'
        verbose_name_plural = 'Requirements'

    def __str__(self):
        return self.name 


class Offer(models.Model):
    name = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    contract = models.ManyToManyField(Contract)
    requirements = models.ManyToManyField(Requirements)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    remote = models.BooleanField(default=False)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def return_requirements(self):
        count = Offer.requirements.through.objects.filter(offer=self).count()
        if count >= 1:
            first_requirements = Offer.requirements.through.objects.filter(
                offer=self
                ).first().requirements.name
            return f"{first_requirements} and {count} other requirement/s"
        return first_requirements
    
    @property
    def salary(self):
        if self.salary_from is None and self.salary_to is None:
            return "Niezdefiniowana"
        elif self.salary_from is None:
            return f"do {self.salary_to} PLN"
        elif self.salary_to is None:
            return f"od {self.salary_from} PLN"
        else:
            return f"{self.salary_from} - {self.salary_to} PLN"
    
    @property 
    def return_localization(self):
        if self.remote == True:
            return f"{self.localization} / remote"
        else:
            return f"{self.localization}"

    class Meta:
        ordering = ('name',)
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'

    def __str__(self):
        return self.name


class Application(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    message = models.CharField(max_length=1000)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    expected_pay = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    portfolio = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    cv = models.FileField(upload_to='resumes', null=True, blank=True)

    @property
    def return_full_name(self):
        return f"{self.first_name} {self.last_name}"