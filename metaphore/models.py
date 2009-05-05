from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import pre_save

from django.contrib.contenttypes.models import ContentType

from metadata.models import MetaDataAbstractBase

class Post(MetaDataAbstractBase):
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
    
    content_type = models.ForeignKey(ContentType, editable=False)
    
    @models.permalink
    def get_absolute_url(self):
        param_dict = { 'year'  : self.publish_date.year,
                       'month' : self.publish_date.month,
                       'day'   : self.publish_date.day,
                       'slug'  : self.slug }
        #from metaphore.urls import info_dict
        #param_dict.update(info_dict)
        return ('metaphore-object-detail', (), param_dict)

    def content(self):
        return self.content_type.model_class().objects.get(post=self)

def _pre_save(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    instance.content_type = ct

class PostAbstractBase(Post):
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        super(PostAbstractBase, self).__init__(*args, **kwargs)
        pre_save.connect(_pre_save, sender=self.__class__)
    
    post = models.OneToOneField('Post', parent_link=True, editable=False, primary_key=True, db_index=True)

class Article(PostAbstractBase):
    text = models.TextField()

class Download(PostAbstractBase):
    download = models.FileField(upload_to='downloads')