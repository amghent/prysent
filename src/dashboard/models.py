from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class OrganizationalUnit(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)  # Not used for now

    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name_plural = "Organizational Units"


class Dashboard(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True, primary_key=True)
    order = models.PositiveIntegerField(null=False, default=0)
    name = models.CharField(max_length=100, null=False, blank=False)  # Used in directory structure
    menu = models.CharField(max_length=30, null=False, blank=False)

    owner = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name_plural = "Dashboards"


class DataPage(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name_plural = "Data Pages"


class CardboxType(Model):
    slug = models.CharField(max_length=10, null=False, blank=False, unique=True, primary_key=True)
    # Used in sample data (large, medium, small, tiny)
    width = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name_plural = "Cardbox Types"


class Cardbox(Model):
    row = models.PositiveIntegerField(null=False, default=0)
    order = models.PositiveIntegerField(null=False, default=0)
    type = models.ForeignKey(CardboxType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=50, null=False, blank=False, default="400px")
    notebook = models.CharField(max_length=1024, null=False, blank=False)  # The file to load, including directories
    scroll = models.BooleanField(null=False, default=False)

    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_page} - {self.notebook}"

    class Meta:
        verbose_name_plural = "Cardboxes"


class Link(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    order = models.PositiveIntegerField(null=False, default=0)
    menu = models.CharField(max_length=30, null=False, blank=False)

    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        abstract = True


class Block(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True, primary_key=True)
    order = models.PositiveIntegerField(null=False, default=0)
    menu = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        abstract = True


class Block1(Block):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Menu Blocks Level 1"


class Block2(Block):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Menu Blocks Level 2"


class Link1(Link):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Menu Links Level 1"


class Link2(Link):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Menu Links Level 2"


class Link3(Link):
    block2 = models.ForeignKey(Block2, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Menu Links Level 3"


class UploadFile(Model):
    dashboard = models.CharField(max_length=256, null=False, blank=False)
    block_1 = models.CharField(max_length=256, null=False, blank=False)
    block_2 = models.CharField(max_length=256, null=False, blank=False)
    menu = models.CharField(max_length=256, null=False, blank=False)
    notebook = models.FileField(upload_to="upload/")

    class Meta:
        verbose_name_plural = "Upload Files"
