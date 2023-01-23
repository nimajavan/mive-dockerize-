from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('api/v1/', include('account.urls', namespace='account')),
    path('api/v1/', include('product.urls', namespace='product')),
    path('api/v1/', include('order.urls', namespace='order')),
    path('api/v1/', include('ticket.urls', namespace='ticket')),
]
if settings.DEBUG:
    urlpatterns += [path('api-auth/', include('rest_framework.urls')),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)