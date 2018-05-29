from django.db import models
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _

from modeltranslation.fields import TranslationField

from prometheus.db.enumerates import StatusEnum


CREATED_VERBOSE = _('Created')
UPDATED_VERBOSE = _('Updated')
LASTMOD_FIELDS = ('created', 'updated')
UTIL_FIELDS = ('id', 'ordering', 'status')


class BaseQuerySet(QuerySet):
    def published(self):
        return self.filter(status__exact=StatusEnum.PUBLIC)

    def hidden(self):
        return self.filter(status__exact=StatusEnum.HIDDEN)

    def draft(self):
        return self.filter(status__exact=StatusEnum.DRAFT)


BaseManager = Manager.from_queryset(BaseQuerySet)
BaseManager.use_for_related_fields = True


class BasicModel(models.Model):
    objects = Manager()
    translation_fields = tuple()

    def collect_fields(self):
        fields = []
        has_status = False
        has_ordering = False
        has_last_mod = False

        for field in self._meta.fields:
            if field.attname == 'status':
                has_status = True

            if field.attname == 'ordering':
                has_ordering = True

            if field.attname in LASTMOD_FIELDS:
                has_last_mod = True
                continue

            if field.attname in UTIL_FIELDS:
                continue

            if isinstance(field, TranslationField):
                continue

            if isinstance(field, ForeignKey):
                fields.append(field.attname.replace('_id', ''))
            else:
                fields.append(field.attname)

        if has_status:
            fields.append('status')

        if has_ordering:
            fields.append('ordering')

        if has_last_mod:
            fields.extend(LASTMOD_FIELDS)

        return fields

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True


class LastModMixin(models.Model):
    """Abstract model for all models with created / updated fields"""
    created = models.DateTimeField(CREATED_VERBOSE, auto_now_add=True, db_index=True)
    updated = models.DateTimeField(UPDATED_VERBOSE, auto_now=True)

    class Meta:
        abstract = True


class StatusOrderingMixin(models.Model):
    """Abstract model for all objects"""
    ordering = models.IntegerField(_('Ordering'), default=0, db_index=True)
    status = models.SmallIntegerField(
        _('Status'),
        default=StatusEnum.PUBLIC,
        choices=StatusEnum.get_choices()
    )

    class Meta:
        abstract = True


class BaseModel(BasicModel, LastModMixin, StatusOrderingMixin):
    """abstract model class for all models having last-mod fields and status with ordering"""
    objects = BaseManager()

    class Meta:
        abstract = True


class DeletableManager(models.Manager):
    def get_queryset(self):
        return super(DeletableManager, self).get_queryset().filter(is_deleted=False)


class VirtualDeletableMixin(models.Model):
    """Virtually removing of objects by checking is_deleted flag"""
    is_deleted = models.BooleanField(_('Deleted'), default=False)
    objects = Manager()
    existing_objects = DeletableManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class ArchivableManager(models.Manager):
    def get_queryset(self):
        return super(ArchivableManager, self).get_queryset().filter(is_archived=False)


class ArchivableMixin(models.Model):
    """Archives mixin"""
    is_archived = models.BooleanField(_('Archived'), default=False)
    objects = Manager()
    existing_objects = ArchivableManager()

    def archive(self, *args, **kwargs):
        self.is_archived = True
        self.save()

    def unarchive(self):
        self.is_archived = False
        self.save()

    class Meta:
        abstract = True


class BaseHandbookModel(VirtualDeletableMixin, BaseModel):
    title = models.CharField(_('Title'), max_length=255, unique=True)

    translation_fields = ('title',)

    objects = BaseManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
