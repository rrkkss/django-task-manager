from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    ## propojeni s base appkou a urls.py modulem
    path('', include('base.urls'))
]
