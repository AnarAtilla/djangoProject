from django.contrib import admin
from django.urls import path, include
from djangoProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.djangohome, name='djangohome'),
    path('library/', include('library.urls')),
    path('task_manager/', include('task_manager.urls')),
]