from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class OrganizationalUnit(Model):
    name = models.CharField(max_length=50, null=False, blank=False)  # Not used for now
    slug = models.CharField(max_length=25, null=False, blank=False)  # Used in directory structure

    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.slug}"


class Dashboard(Model):
    name = models.CharField(max_length=100, null=False, blank=False)  # Not used for now
    slug = models.CharField(max_length=25, null=False, blank=False)   # Used in directory structure
    menu = models.CharField(max_length=30, null=False, blank=False)

    owner = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"


class NotebookPage(Model):
    slug = models.CharField(max_length=25, null=False, blank=False)  # Not used for now
    title = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.slug}"


class CardboxType(Model):
    slug = models.CharField(max_length=10, null=False, blank=False)  # Used in sample data (large, medium, small, tiny)
    width = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.slug}"


class Cardbox(Model):
    row = models.IntegerField(null=False, default=0)
    order = models.IntegerField(null=False, default=0)
    type = models.ForeignKey(CardboxType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    icon = models.CharField(max_length=100, null=True, blank=True)
    height = models.IntegerField(null=False, default=400)
    notebook = models.CharField(max_length=256, null=False, blank=False)

    notebook_page = models.ForeignKey(NotebookPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.notebook_page}"


class Level1Link(Model):
    slug = models.CharField(max_length=256, null=False, blank=False)  # Used as notebook file name
    menu = models.CharField(max_length=30, null=False, blank=False)

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    notebook_page = models.ForeignKey(NotebookPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"


class Level1Menu(Model):
    slug = models.CharField(max_length=256, null=False, blank=False)  # Not used for now
    menu = models.CharField(max_length=30, null=False, blank=False)

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"
