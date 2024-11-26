from django.urls import path
from BookWeb_demo.books import views
from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    ProfileDetailView
)

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),  # Profile details
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('blogs/', BlogPostListView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('blogs/new/', BlogPostCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog-edit'),
    path('blogs/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),


]
