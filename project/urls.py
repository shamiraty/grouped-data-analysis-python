from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('dashboard/', admin.site.urls),
     path('', include("app.urls")),
     path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
]
