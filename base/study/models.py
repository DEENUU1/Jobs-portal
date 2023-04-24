from django.db import models


class Category(models.Model):
    """  """
    name = models.CharField(max_length=50)


class Resources(models.Model):
    """ """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.URLField()
    date_created = models.DateTimeField(auto_created=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

