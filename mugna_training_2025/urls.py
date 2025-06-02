"""
URL configuration for mugna_training_2025 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from mugna_training_2025.views import index, current_datetime, offset_time
from mugna_training_2025.views import add_2, add_3, add_n, validdate

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", index, name="index"),
    path("time/", current_datetime),
    path("offset/<int:offset>", offset_time),
    path("math/<path:nums>", add_n),
    path("valid-date/<int:year>/<int:month>/<int:day>", validdate),
]
