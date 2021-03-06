from django.contrib.admin import ModelAdmin


class SuperUserDeletableAdminMixin(object):
    @staticmethod
    def has_delete_permission(request, obj=None):
        return request.user.is_superuser


class BaseModelAdmin(ModelAdmin):
    """Base admin class for BaseModel"""
    list_display = ('id', 'status', 'ordering', 'created')
    list_editable = ('status', 'ordering')
    list_filter = ('status',)
    ordering = ('ordering',)
    readonly_fields = ('created', 'updated')
    search_fields = ['=id']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BaseModelAdmin, self).get_fieldsets(request, obj=obj)

        for field in ('created', 'updated'):
            if field not in fieldsets[0][1]['fields']:
                fieldsets[0][1]['fields'].append(field)

        return fieldsets


class VirtualDeleteAdminMixin(object):
    readonly_fields = ('is_deleted',)
    list_filter = ('is_deleted',)

    @staticmethod
    def suit_row_attributes(obj, request):
        return {'class': 'is-deleted' if obj.is_deleted else ''}


class BaseHandbookModelAdmin(SuperUserDeletableAdminMixin, BaseModelAdmin):
    """Base handbook model admin"""
    list_display = ('id', 'title', 'status', 'ordering', 'created')
    list_display_links = ('id', 'title')
    readonly_fields = BaseModelAdmin.readonly_fields + ('is_deleted',)
    search_fields = BaseModelAdmin.search_fields + ['title']
