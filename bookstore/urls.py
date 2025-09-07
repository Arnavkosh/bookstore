from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),   
    path('cart/', include('cart.urls')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('', include('pages.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
