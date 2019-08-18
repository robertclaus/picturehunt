from django.db import models
import base64
from PIL import Image
from io import BytesIO
from django.conf import settings


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
        return f"{self.segment} - {self.order_index} [{self.id}]"

    def save(self, *args, **kwargs):
        # Save the image file and get the url
        super(Clue, self).save(*args, **kwargs)
        self.generate_permanent_content()
        super(Clue, self).save(*args, **kwargs)

    def generate_permanent_content(self):
        max_dimension = settings.MAX_IMAGE_DIMENSION

        self.temp_img.open(mode="rb")
        original_image = Image.open(self.temp_img)
        w, h = original_image.size

        w_ratio = max_dimension / w
        h_ratio = max_dimension / h

        if h_ratio > w_ratio:
            max_size = (w * w_ratio, h * w_ratio)
        else:
            max_size = (w * h_ratio, h * h_ratio)

        original_image.thumbnail(max_size, Image.ANTIALIAS)

        buffer = BytesIO()
        original_image.save(buffer, format="PNG")
        content = buffer.getvalue()

        encoded_string = base64.b64encode(content).decode('utf-8')
        encoded_string = f"data:image/png;base64, {encoded_string}"
        self.img_content = encoded_string


class CompletedClue(models.Model):
    clue = models.ForeignKey('Clue', null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, blank=True)
    guess = models.TextField(null=True, blank=True)
    correct = models.BooleanField()

    def __str__(self):
        return f"{self.team} - {self.clue} - {self.guess}"


class SegmentOrder(models.Model):
    index = models.IntegerField(null=True, blank=True)
    segment = models.ForeignKey('Segment', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.index} - {self.segment} [{self.id}]"


class Path(models.Model):
    segment_order = models.ManyToManyField('SegmentOrder', blank=True)

    def __str__(self):
        return f"Path [{self.id}]"
