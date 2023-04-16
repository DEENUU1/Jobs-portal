from django.db import models


class Position(models.Model):
    POSITION = (
        ("python", "Python"),
        ("java", "Java"),
        ("c", "C"),
        (".net", ".NET"),
        ("javascript", "JavaScript"),
        ("php", "PHP"),
        ("scala", "Scala"),
        ("mobile", "Mobile"),
        ("testing", "Testing"),
        ("devops", "DevOps"),
        ("ux/ui", "UX/UI"),
        ("game", "Game"),
        ("data", "Data"),
        ("golang", "Golang"),
        ("security", "Security"),
    )
    position = models.ManyToManyField(choices=POSITION, max_length=50)


class Level(models.Model):
    LEVEL = (
        ("intern", "Intern"),
        ("junior", "Junior"),
        ("middle", "Middle"),
        ("senior", "Senior"),
        ("expert", "Expert")
    )
    name = models.CharField(choices=LEVEL, max_length=50)


class Country(models.Model):
    name = models.CharField(max_length=50)


class Localization(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)


class Contract(models.Model):
    CONTRACT = (
        ("uop", "Umowa o pracę"),
        ("uz", "Umowa zlecenie"),
        ("b2b", "Kontrakt b2b"),
    )

    contract = models.ManyToManyField(choices=CONTRACT, max_length=50)