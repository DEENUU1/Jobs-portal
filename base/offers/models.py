from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50)


class Level(models.Model):
    name = models.CharField(max_length=50)


class Country(models.Model):
    name = models.CharField(max_length=50)
