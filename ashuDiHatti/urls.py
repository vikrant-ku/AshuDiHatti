from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from shop.views import error
from . import settings

# from django.views.static import serve
# from django.conf.urls import url


admin.site.site_header = 'Ashu Di Hatti admin'
admin.site.site_title = 'Ashu Di Hatti admin'
admin.site.site_url = ' http://127.0.0.1:8000/'
admin.site.index_title = 'Ashu Di Hatti administration'
admin.empty_value_display = '**Empty**'

handler404 = error.error_404
handler500 = error.error_500

# url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
# url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('rohar/tech/ashu/di/hatti/api/', include('api.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


