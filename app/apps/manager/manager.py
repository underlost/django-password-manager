import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class EntryManager(models.Manager):
    def public(self):
        return super(EntryManager, self).get_queryset().filter(is_public=True)
