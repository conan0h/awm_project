from django.contrib.gis.db import models

class WikipediaArticle(models.Model):
    pageid = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    index = models.IntegerField(null=True)
    coordinates_lat = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    coordinates_lon = models.DecimalField(max_digits=10, decimal_places=6, null=True)
