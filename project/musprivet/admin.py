from django.contrib import admin
from .models import Category, Subcategory, Tag, ServiceCongratsByName, ServiceCongratsByTag, ServiceSongs, \
    ServiceAdvertisement, Review, Name, PoemByName, PaymentServiceByName, PaymentService, Blog, ServiceSongsVideo, \
    SongRequest, ServiceVideoAdvertisement, ServiceAdClipPrice, ServiceAdClipRequest, ServiceAdMusicRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image')
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug', 'subcategory')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ServiceCongratsByTag)
class ServiceCongratsByTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'tag', 'slug', 'audio_file')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PoemByName)
class PoemByNameAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'text', 'name', 'tag')
    search_fields = ('title',)

@admin.register(ServiceCongratsByName)
class ServiceCongratsByNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'poem', 'category', 'audio_file')
    search_fields = ('title',)

@admin.register(ServiceSongs)
class ServiceSongsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'image_field', 'audio_file')
    search_fields = ('title',)

@admin.register(ServiceSongsVideo)
class ServiceSongsVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'type', 'video_mp4', 'video_webm', 'image_field')
    search_fields = ('title',)

@admin.register(SongRequest)
class SongRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'message', 'created_at')
    search_fields = ('name',)

@admin.register(ServiceAdvertisement)
class ServiceAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'tag', 'audio_file')
    search_fields = ('title',)

@admin.register(ServiceVideoAdvertisement)
class ServiceVideoAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'tag', 'video_mp4', 'video_webm', 'image_field')
    search_fields = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'text', 'category')
    search_fields = ('name',)

@admin.register(Blog)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_field', 'text', 'date_field')
    search_fields = ('title',)

@admin.register(PaymentService)
class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'phone', 'email', 'congratulation', 'created_at', 'price')
    search_fields = ('service',)

@admin.register(PaymentServiceByName)
class PaymentServiceByNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'phone', 'email', 'congratulation', 'created_at', 'price')
    search_fields = ('service',)

@admin.register(ServiceAdClipPrice)
class ServiceAdClipPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'description', 'type', 'timing')
    search_fields = ('title',)

@admin.register(ServiceAdClipRequest)
class ServiceAdClipRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'timing', 'service', 'audio_file', 'created_at')
    search_fields = ('name',)

@admin.register(ServiceAdMusicRequest)
class ServiceAdMusicRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'service', 'audio_file', 'created_at')
    search_fields = ('name',)
