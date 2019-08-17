from django.db import models
import base64

# Create your models here.
class User(models.Model):
    name = models.TextField(null=True, blank=True)
    current_team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)
    logged_in = models.BooleanField()

    def __str__(self):
        return f"{self.name} [{self.id}]"


class Team(models.Model):
    name = models.TextField(null=True, blank=True)
    current_clue = models.ForeignKey('Clue', null=True, blank=True, on_delete=models.CASCADE)
    path = models.ForeignKey('Path', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} [{self.id}]"


class Segment(models.Model):
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.id}]"


class Clue(models.Model):
    text = models.TextField(null=True, blank=True)
    temp_img = models.ImageField(upload_to="site_media", null=True, blank=True)
    segment = models.ForeignKey('Segment', null=True, blank=True, on_delete=models.CASCADE, related_name="clues")
    order_index = models.IntegerField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    img_content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.segment.name} - {self.order_index} [{self.id}]"

    def save(self, *args, **kwargs):
        # Save the image file and get the url
        super(Clue, self).save(*args, **kwargs)

        # Save the image file content directly for long term storage
        with open(self.temp_img.url, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            self.img_content = encoded_string
            super(Clue, self).save(*args, **kwargs)


class CompletedClue(models.Model):
    clue = models.ForeignKey('Clue', null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)


class SegmentOrder(models.Model):
    index = models.IntegerField(null=True, blank=True)
    segment = models.ForeignKey('Segment', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order_index} - {self.segment.name} [{self.id}]"


class Path(models.Model):
    segment_order = models.ManyToManyField('SegmentOrder', blank=True)

    def __str__(self):
        return f"Path [{self.id}]"
