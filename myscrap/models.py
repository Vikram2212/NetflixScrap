from django.db import models


class Search(models.Model):
    search = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{}'.format(self.search)
