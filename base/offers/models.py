from django.db import models
from accounts.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField


class Position(models.Model):
    """
    The `Position` class is a Django model used to represent a job position.
    Attributes:
        - position_name (CharField): A character field that represents the name of the position.
    """
    position_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('position_name',)
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.position_name


class Level(models.Model):
    """
    The `Level` class is a Django model used to represent a experience level of a job.
    Attributes:
        - level_name (CharField): A character field that represents the name of the level.
    """
    level_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('level_name',)
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'

    def __str__(self):
        return self.level_name


class Country(models.Model):
    """
    The `Country` class is a Django model used to represent a Country.
    Attributes:
        - name (CharField): A character field that represents the name of the country.
    """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name
    

class Localization(models.Model):
    """
    The `Localization` class is a Django model used to represent a city.
    Attributes:
        - city (CharField): A character field that represents the name of the position.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)

    class Meta:
        ordering = ('city',)
        verbose_name = 'Localization'
        verbose_name_plural = 'Localizations'

    def __str__(self):
        return self.city


class Contract(models.Model):
    """
    The `Contract` class is a Django model used to represent a job contract type.
    Attributes:
        - contract_type (CharField): A character field that represents the name of contract type.
    """
    contract_type = models.CharField(max_length=50)

    class Meta:
        ordering = ('contract_type',)
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

    def __str__(self):
        return self.contract_type


class Requirements(models.Model):
    """
    The `Requirements` class is a Django model used to represent a requirements.
    Attributes:
        - name (CharField): A character field that represents the name of the requirement.
    """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Requirement'
        verbose_name_plural = 'Requirements'

    def __str__(self):
        return self.name 


class Offer(models.Model):
    """
    The `Offer` class is a Django model used to represent a job offer.

    Attributes:
        - name (CharField): A character field that represents the name of the offer.
        - position (ForeignKey): A foreign key that represents the position associated with the offer.
        - level (ForeignKey): A foreign key that represents the level associated with the offer.
        - contract (ManyToManyField): A many-to-many field that represents the contracts associated with the offer.
        - requirements (ManyToManyField): A many-to-many field that represents the requirements associated with the
          offer.
        - localization (ForeignKey): A foreign key that represents the localization associated with the offer.
        - address (CharField): A character field that represents the address associated with the offer.
        - description (CharField): A character field that represents the description associated with the offer.
        - salary_from (IntegerField): An integer field that represents the minimum salary for the offer.
        - salary_to (IntegerField): An integer field that represents the maximum salary for the offer.
        - date_created (DateTimeField): A datetime field that represents the date the offer was created.
        - remote (BooleanField): A boolean field that represents whether the offer is remote.
        - company (ForeignKey): A foreign key that represents the company associated with the offer.
    """
    name = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    contract = models.ManyToManyField(Contract)
    requirements = models.ManyToManyField(Requirements)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    remote = models.BooleanField(default=False)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def return_full_address(self) -> str:
        """
        A property that returns the full address of the offer, including localization and address.
        """
        return f"{self.localization}, {self.address}"

    @property
    def return_contract(self) -> str:
        """
        A property that returns a string representation of the contracts associated with the offer.
        """
        all_contracts = []
        for contract in self.contract.all():
            all_contracts.append(contract.contract_type)
        return ', '.join(all_contracts)

    @property
    def return_all_requirements(self) -> str:
        """
        A property that returns a string representation of all the requirements associated with the offer.
        """
        all_requirements = []
        for requirement in self.requirements.all():
            all_requirements.append(requirement.name)
        return ', '.join(all_requirements)

    @property
    def return_requirements(self) -> str:
        """
        A property that returns a string representation of the first requirement associated with the offer and the
        count of the remaining requirements.
        """
        count = Offer.requirements.through.objects.filter(offer=self).count()
        if count >= 1:
            first_requirements = Offer.requirements.through.objects.filter(
                offer=self
                ).first().requirements.name
            return f"{first_requirements} and {count} other requirement/s"
        return first_requirements
    
    @property
    def salary(self) -> str:
        """
        A property that returns a string representation of the salary range for the offer.
        """
        if self.salary_from is None and self.salary_to is None:
            return "Niezdefiniowana"
        elif self.salary_from is None:
            return f"do {self.salary_to} PLN"
        elif self.salary_to is None:
            return f"od {self.salary_from} PLN"
        else:
            return f"{self.salary_from} - {self.salary_to} PLN"
    
    @property 
    def return_localization(self) -> str:
        """
        A property that returns a string representation of the localization associated with the offer,
        including 'remote' if applicable.
        """
        if self.remote:
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
    """
    A model to represent a job application.
    Attributes:
        - first_name (str): The applicant's first name.
        - last_name (str): The applicant's last name.
        - email (str): The applicant's email address.
        - phone_number (phonenumbers.PhoneNumber): The applicant's phone number.
        - message (str): A message from the applicant to the employer.
        - offer (Offer): The job offer the applicant is applying for.
        - expected_pay (decimal.Decimal): The expected pay of the applicant.
        - date_created (datetime.datetime): The date and time the application was created.
        - portfolio (str, optional): A URL to the applicant's portfolio.
        - linkedin (str, optional): A URL to the applicant's LinkedIn profile.
        - cv (django.core.files.File, optional): A file upload of the applicant's CV/resume.
        - answer (bool): A flag indicating whether the application has been answered by the employer.
    """
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
    answer = models.BooleanField(default=False)

    @property
    def return_full_name(self) -> str:
        """
        Returns the applicant's full name as a string.
        """
        return f"{self.first_name} {self.last_name}"
    
    def update_answer(self, answer):
        """
        Updates the answer flag of the application to the given value.
        """
        self.answer = answer
        self.save()
