from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import *
#---------------------------------------------------------------------#
class ProvTypeResource(resources.ModelResource):
    class Meta:
        model = ProvType

class ProvTypeAdmin(ImportExportActionModelAdmin):
    resource_class = ProvTypeResource
    list_display = (
        "rut",
        "name",
    )
    search_fields = (
        "rut",
        "name",
    )
    list_per_page = 25


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article

class ArticleAdmin(ImportExportActionModelAdmin):
    resource_class = ArticleResource
    list_display = (
        "cod_sap",
        "name",
    )
    search_fields = (
        "cod_sap",
        "name",
    )
    list_per_page = 25
#---------------------------------------------------------------------#
admin.site.register(Article, ArticleAdmin)
admin.site.register(ProvType, ProvTypeAdmin)
admin.site.register(DocXml)