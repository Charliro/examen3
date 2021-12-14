from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('appoint', views.appoint),
    path('toadd', views.toadd),
    path('add', views.add),
    path('update/<appoint_id>', views.update),
    path('logout', views.logout),
    path('delete/<appoint_id>', views.delete),
    path('edit_appoint/<appoint_id>', views.edit_appoint),
]
