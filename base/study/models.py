from django.db import models


class Category(models.Model):
    """  """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Resources(models.Model):
    """ """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.URLField()
    date_created = models.DateTimeField(auto_created=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __str__(self):
        return self.name