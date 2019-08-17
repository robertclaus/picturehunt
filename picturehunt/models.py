from django.db import models


# Create your models here.
class User(models.Model):
    name = models.TextField(null=True, blank=True)
    current_team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)
    logged_in = models.BooleanField()


class Team(models.Model):
    name = models.TextField(null=True, blank=True)
    current_clue = models.ForeignKey('Clue', null=True, blank=True, on_delete=models.CASCADE)
    path = models.ForeignKey('Path', null=True, blank=True, on_delete=models.CASCADE)


class Segment(models.Model):
    name = models.TextField(null=True, blank=True)


class Clue(models.Model):
    text = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="site_media", null=True, blank=True)
    segment = models.ForeignKey('Segment', null=True, blank=True, on_delete=models.CASCADE)
    order_index = models.IntegerField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)


class CompletedClue(models.Model):
    clue = models.ForeignKey('Clue', null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)


class SegmentOrder(models.Model):
    index = models.IntegerField(null=True, blank=True)
    segment = models.ForeignKey('Segment', null=True, blank=True, on_delete=models.CASCADE)


class Path(models.Model):
    segment_order = models.ManyToManyField('SegmentOrder', blank=True)
