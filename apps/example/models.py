import base64

from django.conf import settings
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=80)
    url = models.TextField()
    content_html = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, related_name='articles_user', blank=True, null=True)

    def __str__(self):
        return self.title

    def author_name(self):
        return self.author.username

    class Meta:
        ordering = ['-date_published']

    def save(self, *args, **kwargs):
        if self.image:
            logo = self.image.open()
            self.org_logo_b64 = base64.b64encode(logo.read())
        return super(Article, self).save(*args, **kwargs)


class ArticleTag(models.Model):

    article = models.ForeignKey(Article, models.CASCADE, related_name='article_tags')
    tag = models.ForeignKey(Tag, models.PROTECT, related_name='article_tags')

    def article_title(self):
        return self.article.title

    def tag_name(self):
        return self.tag.name

    class Meta:
        unique_together = ('article', 'tag')
