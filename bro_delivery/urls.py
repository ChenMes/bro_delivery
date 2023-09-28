"""
URL configuration for bro_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from bro_delivery_app.view_sets import *

router = DefaultRouter()
router.register('api/deliveries', DeliveryViewSet)
router.register('api/restaurants', RestaurantViewSet)
router.register('api/customers', CustomerViewSet)
router.register('api/users', RestaurantViewSet)
router.register('api/addresses', AddressViewSet)
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/tokens', ExtendedTokenObtainPairView.as_view()),
    path('api/tokens/refresh', TokenRefreshView.as_view()),
    path('api/me', me),
    path('api/google-auth', google_login),
    path('api/addresses_street', get_address_delivery),
    path('api/customers_phone', get_customer_phone),
    path('api/delivery_guy', get_delivery_guy),
    path('api/restaurant_deliveries', restaurant_deliveries),
    path('api/delivery_guy_deliveries', delivery_guy_deliveries)
    # path('profile/img', upload_profile_img),
    # path('profile/img/presigned', upload_profile_img_url),
    # path('profile/img/done', upload_profile_img_done),
]
urlpatterns.extend(router.urls)
