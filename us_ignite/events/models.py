from django.db import models
from django.core.urlresolvers import reverse

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.common.fields import AutoUUIDField
from us_ignite.events import managers


class Event(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )

    name = models.CharField(max_length=500)
    slug = AutoUUIDField(unique=True, editable=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    website = models.URLField(max_length=500, blank=True)
    image = models.ImageField(upload_to="events", blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    venue = models.TextField()
    description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    hubs = models.ManyToManyField('hubs.Hub')
    user = models.ForeignKey('auth.User')
    is_featured = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # mamagers
    objects = models.Manager()
    published = managers.EventPublishedManager()

    class Meta:
        ordering = ('-is_featured', 'start_datetime')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug])

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_owner(self, user):
        return self.user == user
