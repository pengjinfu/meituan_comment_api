"""
URL configuration for meituan_comment_api project.

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
from django.urls import path
from client import views

urlpatterns = [
    path('malls/', views.Malls.as_view()),
    path('malls/<int:mall_id>/', views.MallDetail.as_view()),
    path('activation/', views.Activation.as_view()),
    path('comments/<int:mall_id>/', views.Comments.as_view()),
    path('orders/<int:comment_id>/', views.OrderDetail.as_view())
]
