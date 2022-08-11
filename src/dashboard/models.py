from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class OrganizationalUnit(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)  # Not used for now

    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.slug}"


class Dashboard(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)  # Used in directory structure
    menu = models.CharField(max_length=30, null=False, blank=False)

    owner = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"


class DataPage(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.slug}"


class CardboxType(Model):
    slug = models.CharField(max_length=10, null=False, blank=False, unique=True, primary_key=True)
    # Used in sample data (large, medium, small, tiny)
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
    notebook = models.CharField(max_length=1024, null=False, blank=False)  # The file to load, including directories

    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_page}"


class Link(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    menu = models.CharField(max_length=30, null=False, blank=False)

    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        abstract = True


class Block(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    menu = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        abstract = True


class Block1(Block):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)


class Block2(Block):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)


class Link1(Link):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)


class Link2(Link):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)


class Link3(Link):
    block2 = models.ForeignKey(Block2, on_delete=models.CASCADE)






