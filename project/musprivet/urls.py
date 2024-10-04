from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .models import ServiceCongratsByTag
from .views import ServiceCongratsByTagListView, ServiceCongratsByTagDetailView, PoemByNameDetailView, \
    ServiceSongsListView, ServiceAdvertisementListView, AdvertisementView, AboutUsView, UserManualView, RefundView

app_name = 'musprivet'

urlpatterns = [
    path('mus-pozdrav/', ServiceCongratsByTagListView.as_view(queryset=ServiceCongratsByTag.objects.none()), name='congrat_list_default'),
    path('mus-pozdrav/<slug:tag_slug>', ServiceCongratsByTagListView.as_view(), name='congrat_list'),
    path('mus-pozdrav/<slug:tag_slug>/<slug:congrat_slug>', ServiceCongratsByTagDetailView.as_view(), name='congrat_detail'),
    path('mus-pozdrav/<slug:tag_slug>/name/<slug:name_slug>', PoemByNameDetailView.as_view(), name='name_poem_detail'),
    path('podarit-pesnu/', ServiceSongsListView.as_view(), name='song_list'),
    path('audioreklama/<slug:subcategory_slug>', ServiceAdvertisementListView.as_view(), name='ads_list'),
    path('audioreklama/', AdvertisementView.as_view(), name='audioreklama'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('user-manual/', UserManualView.as_view(), name='user_manual'),
    path('refund/', RefundView.as_view(), name='refund'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
