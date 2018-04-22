import markdown
import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .utils import AESCipher
from .manager import EntryManager

IS_PUBLIC_CHOICES = ((True, 'Everyone'), (False, 'Just me'),)

class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='entries', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    comment_html = models.TextField(null=True, blank=True)
    expires = models.DateField(null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(help_text=_("Who can see this entry?"), choices=IS_PUBLIC_CHOICES, default=True)
    objects = EntryManager()

    class Meta:
        ordering = ('title', 'date_updated')
        verbose_name_plural = "Entries"

    def __str__(self):
        return self.title

    def dict(self):
        dic = {}
        dic['id'] = self.id
        dic['title'] = self.title
        dic['url'] = self.url
        dic['username'] = self.username
        dic['password'] = self.password
        dic['comment'] = self.comment
        dic['date_updated'] = str(self.date_updated)
        dic['date_created'] = str(self.date_created)
        dic['expires'] = str(self.expires)
        dic['category'] = self.category.title
        return dic

    @classmethod
    def from_db(self, db, field_names, values):
        new = super(Entry, self).from_db(db, field_names, values)
        # cache value went from the base
        new._old_password = values[field_names.index('password')]
        return new

    def save(self, *args, **kwargs):
        self.comment_html = markdown.markdown(self.comment)
        cipher = AESCipher(settings.MASTER_KEY)
        if self._state.adding:
            # encrypt the password
            self.password = cipher.encrypt(self.password).decode('utf-8')
        else:
            # updating, check if we need to update the stored password
            if self.password and self._old_password:
                decoded = cipher.decrypt(self._old_password)
                if self.password != decoded:
                    # old pass and new don't match, update the password
                    self.password = cipher.encrypt(self.password).decode('utf-8')

        super(Entry, self).save(*args, **kwargs)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

    def entry_count(self):
        total = Entry.objects.filter(category=self).count()
        return total
