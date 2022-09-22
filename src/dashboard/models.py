from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.dispatch import receiver


class OrganizationalUnit(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True)
    name = models.CharField(max_length=50, null=False, blank=False)  # Not used for now
    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name_plural = "Organizational Units"


class Dashboard(Model):
    slug = models.CharField(max_length=25, null=False, blank=False, unique=True)
    order = models.PositiveIntegerField(null=False, default=0, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)  # Used in directory structure
    menu = models.CharField(max_length=30, null=False, blank=False, unique=True)
    owner = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    sync_flag = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Dashboards"


class DataPage(Model):
    slug = models.CharField(max_length=256, null=False, blank=False, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Data Pages"


class CardboxType(Model):
    slug = models.CharField(max_length=10, null=False, blank=False, unique=True)
    # Used in sample data (large, medium, small, tiny)
    width = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Cardbox Types"


class Cardbox(Model):
    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)
    row = models.PositiveIntegerField(null=False, default=0)
    order = models.PositiveIntegerField(null=False, default=0)
    type = models.ForeignKey(CardboxType, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=50, null=False, blank=False, default="400px")
    notebook = models.CharField(max_length=1024, null=False, blank=False)  # The file to load, including directories
    scroll = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.data_page} - {self.notebook} <{self.id}>"

    class Meta:
        verbose_name_plural = "Cardboxes"
        unique_together = ("data_page", "row", "order")


class Link(Model):
    slug = models.CharField(max_length=256, null=False, blank=False)
    order = models.PositiveIntegerField(null=False, default=0)
    menu = models.CharField(max_length=30, null=False, blank=False)
    data_page = models.ForeignKey(DataPage, on_delete=models.CASCADE)
    sync_flag = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Block(Model):
    slug = models.CharField(max_length=256, null=False, blank=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    order = models.PositiveIntegerField(null=False, default=0)
    menu = models.CharField(max_length=30, null=False, blank=False)
    sync_flag = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Block1(Block):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dashboard.slug}_{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Menu Blocks Level 1"

        constraints = [
            models.UniqueConstraint(fields=['dashboard', 'slug'], name='ux_block1_dashboard_slug'),
            models.UniqueConstraint(fields=['dashboard', 'order'], name='ux_block1_dashboard_order'),
            models.UniqueConstraint(fields=['dashboard', 'menu'], name='ux_block1_dashboard_menu'),
        ]


class Block2(Block):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.block1.dashboard.slug}_{self.block1.slug}_{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Menu Blocks Level 2"

        constraints = [
            models.UniqueConstraint(fields=['block1', 'slug'], name='ux_block2_block1_slug'),
            models.UniqueConstraint(fields=['block1', 'order'], name='ux_block2_block1_order'),
            models.UniqueConstraint(fields=['block1', 'menu'], name='ux_block2_block1_menu'),
        ]


class Link1(Link):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dashboard.slug}_{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Menu Links Level 1"

        constraints = [
            models.UniqueConstraint(fields=['dashboard', 'order'], name='ux_link1_dashboard_order'),
        ]


class Link2(Link):
    block1 = models.ForeignKey(Block1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.block1.dashboard.slug}_{self.block1.slug}_{self.slug} <{self.id}>"

    class Meta:
        verbose_name_plural = "Menu Links Level 2"

        constraints = [
            models.UniqueConstraint(fields=['block1', 'order'], name='ux_link2_block1_order'),
        ]


class Link3(Link):
    block2 = models.ForeignKey(Block2, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.block2.block1.dashboard.slug}_{self.block2.block1.slug}_{self.block2.slug}_{self.slug}" \
               f" <{self.id}>"

    class Meta:
        verbose_name_plural = "Menu Links Level 3"

        constraints = [
            models.UniqueConstraint(fields=['block2', 'order'], name='ux_link3_block2_order'),
        ]


@receiver(models.signals.pre_delete, sender=Dashboard)
@receiver(models.signals.pre_delete, sender=DataPage)
@receiver(models.signals.pre_delete, sender=Cardbox)
@receiver(models.signals.pre_delete, sender=Block1)
@receiver(models.signals.pre_delete, sender=Block2)
@receiver(models.signals.pre_delete, sender=Link1)
@receiver(models.signals.pre_delete, sender=Link2)
@receiver(models.signals.pre_delete, sender=Link3)
def handle_deleted_dashboard(sender, instance, **kwargs):
    assert sender  # To avoid JetBrains nagging
    assert kwargs
    print(f"Deleting {instance.__class__.__name__}: {instance}")


@receiver(models.signals.post_delete, sender=Link1)
def handle_deleted_link1(sender, instance, **kwargs):
    assert sender  # To avoid JetBrains nagging
    assert kwargs
    instance.data_page.delete()


@receiver(models.signals.post_delete, sender=Link2)
def handle_deleted_link2(sender, instance, **kwargs):
    assert sender  # To avoid JetBrains nagging
    assert kwargs
    instance.data_page.delete()


@receiver(models.signals.post_delete, sender=Link3)
def handle_deleted_link2(sender, instance, **kwargs):
    assert sender  # To avoid JetBrains nagging
    assert kwargs
    instance.data_page.delete()
