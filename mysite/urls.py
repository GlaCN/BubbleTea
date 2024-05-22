
from django.contrib import admin
from django.urls import path
from bubbleTea import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription/',views.inscription, name = 'inscription'),
    # path('adminRegister',views.adminRegister, name = 'adminRegister'),
    # path('adminLogin', views.adminLogin, name='adminLogin'),
    path('connection/', views.log, name = 'connection'),
    path('profil/',views.profil, name= 'profil'),
    path('allUsers/', views.AllUsers, name='allUsers'),

    path('', views.homepage, name='homepage'),

    path('adminRegister/', views.adminRegister, name='adminRegister'),
    path('adminLogin/', views.adminLogin, name='adminLogin'),

    path('controlDashboard/', views.selectProduct, name='controlDashboard'),

    path('addProduct/', views.addProduct, name='addProduct'),
    path('updateProduct/', views.updateProduct, name='updateProduct'),

    path('products/', views.AllProducts, name='products'),
    path('products/<id>/', views.oneProduct, name='oneProduct'),

    # path('cart/', views.addCart, name='cart')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
