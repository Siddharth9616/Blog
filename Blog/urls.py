from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # API to post a comment
    path('postComment', views.postComment, name="postComment"),
    
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>/', views.blogPost, name='blogpost'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)