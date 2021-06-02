from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('logout', views.logout),
    path('index', views.index),
    path('register', views.register),
    path('item',views.item),
    path('order',views.order),
    path('library',views.library),
    path('sell',views.sell),
    path('sellorder',views.sell_order),
    path('info',views.info)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)