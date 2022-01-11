from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"), 
    path("new_page", views.new_page, name="new_page"), 
    path("delete_page/<str:title>", views.delete_page, name="delete_page"), 
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),  
    path("save_edited_page/<str:title>", views.save_edited_page, name="save_edited_page"),
    path("random_page", views.random_page, name="random_page")  
]
