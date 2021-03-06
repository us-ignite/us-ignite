from django.contrib import admin
from copy import deepcopy
from models import *
# from us_ignite.actionclusters.models import ActionCluster
# from us_ignite.actionclusters.admin import ActionClusterAdmin



class ApplicationURLInline(admin.TabularInline):
    model = ApplicationURL


class ApplicationMediaInline(admin.TabularInline):
    model = ApplicationMedia


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'program', 'slug', 'stage', 'status')
    search_fields = ['name', 'slug', 'summary', 'impact_statement',
                     'assistance', 'team_description', 'notes',
                     'acknowledgments']
    list_filter = ['stage', 'status', 'created', 'categories', 'sector', 'program']
    exclude = ['keywords', 'programs']
    date_hierarchy = 'created'
    filter_horizontal = ("categories", "features")

    inlines = [ApplicationURLInline, ApplicationMediaInline]


# class ActionClusterAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'stage', 'status', 'is_approved')
#     search_fields = ['name', 'slug', 'summary', 'impact_statement',
#                      'assistance', 'team_description', 'notes',
#                      'acknowledgments']
#     list_filter = ['stage', 'status', 'created', 'is_approved', 'community']
#     date_hierarchy = 'created'
#     # inlines = [ActionClusterURLInline, ActionClusterMediaInline]


class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')


class YearAdmin(admin.ModelAdmin):
    list_display = ('year', )


class PageApplicationInline(admin.TabularInline):
    raw_id_fields = ('application', )
    model = PageApplication


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created', )
    list_filter = ('status', 'created', )
    date_hierarchy = 'created'
    inlines = [PageApplicationInline]


# class ActionCluster(ActionCluster):
#     class Meta:
#         proxy = True
#         verbose_name = "Actioncluster"


admin.site.register(Application, ApplicationAdmin)
# admin.site.register(ActionCluster, ActionClusterAdmin)

admin.site.register(Sector, SectorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Page, PageAdmin)