from modeltranslation.translator import translator, TranslationOptions

from .models import *


class TourPlanTranslationOptions(TranslationOptions):
    fields = ('content1', 'content2', 'content3', 'content4', 'content5', 'content6', 'content7')


translator.register(TourPlan, TourPlanTranslationOptions)


class PlacesTranslationOptions(TranslationOptions):
    fields = ('title', 'inf_content')


translator.register(Places, PlacesTranslationOptions)


class TourBlogTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(TourBlog, TourBlogTranslationOptions)


class CitiesTranslationOptions(TranslationOptions):
    fields = ('name', 'info')


translator.register(Cities, CitiesTranslationOptions)


class HotelsTranslationOptions(TranslationOptions):
    fields = ('name', 'info')


translator.register(Hotels, HotelsTranslationOptions)


class Explore_MoreTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(Explore_More, Explore_MoreTranslationOptions)