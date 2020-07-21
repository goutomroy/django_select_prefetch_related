from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.bookstore import views


urlpatterns = [
    path('forward_one_to_one_without_sr/', views.forward_one_to_one_without_sr),
    path('forward_one_to_one_with_sr/', views.forward_one_to_one_with_sr),
    path('backward_one_to_one_without_sr/', views.backward_one_to_one_without_sr),
    path('backward_one_to_one_with_sr/', views.backward_one_to_one_with_sr),
    path('forward_foreign_key_without_sr/', views.forward_foreign_key_without_sr),
    path('forward_foreign_key_with_sr/', views.forward_foreign_key_with_sr),
    path('backward_foreign_key_without_pr/', views.backward_foreign_key_without_pr),
    path('backward_foreign_key_with_pr/', views.backward_foreign_key_with_pr),
    path('forward_many_to_many_without_pr/', views.forward_many_to_many_without_pr),
    path('forward_many_to_many_with_pr/', views.forward_many_to_many_with_pr),
    path('backward_many_to_many_without_pr/', views.backward_many_to_many_without_pr),
    path('backward_many_to_many_with_pr/', views.backward_many_to_many_with_pr),
    path('stores_expensive_books_pr/', views.stores_expensive_books_pr),
    path('stores_expensive_books_pr_efficient/', views.stores_expensive_books_pr_efficient),
]