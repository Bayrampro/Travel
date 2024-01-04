from django.contrib import admin
from .models import *


class CitiesAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_photo', 'velayat']
    list_display_links = ['name']
    search_fields = ['name', 'velayat']
    list_filter = ['velayat']
    prepopulated_fields = {'slug': ('name',)}
    group_fieldsets = True


class HotelsAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'cost', 'stars']
    list_display_links = ['name']
    search_fields = ['name', 'city']
    list_filter = ['city', 'stars']
    prepopulated_fields = {'slug': ('name',)}
    group_fieldsets = True


class PlacesAdmin(admin.ModelAdmin):
    list_display = ['title', 'tour_plan', 'cost']
    list_display_links = ['title']
    search_fields = ['title', 'tour_plan']
    list_filter = ['tour_plan']
    prepopulated_fields = {'slug': ('title',)}
    group_fieldsets = True


class TourBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
    list_display_links = ['title']
    search_fields = ['title', 'content']
    list_filter = ['title']
    readonly_fields = ['views', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    group_fieldsets = True


class Explore_MoreAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
    list_display_links = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    group_fieldsets = True


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'date']
    list_display_links = ['user']
    list_filter = ['date', 'tour']
    search_fields = ['date', 'tour']
    readonly_fields = ['date']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']
    list_display_links = ['user']
    list_filter = ['user', 'email']
    search_fields = ['email', 'user']
    readonly_fields = ['user', 'email', 'subject']


admin.site.register(Places, PlacesAdmin)
admin.site.register(TourPlan)
admin.site.register(TourBlog, TourBlogAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Hotels, HotelsAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Explore_More, Explore_MoreAdmin)
admin.site.register(Feedback, FeedbackAdmin)
