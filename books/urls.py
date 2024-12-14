from django.urls import path
from BookWeb_demo.books import views
from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    ProfileDetailView, ProductList, BlogPostList,
)




urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
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

    path('order/manage/<int:pk>/', views.manage_order, name='manage-order'),
    path('product/manage/<int:pk>/', views.manage_product, name='manage-product'),
    path('customer/update/<int:pk>/', views.update_customer, name='update-customer'),

    path('products/', ProductList.as_view(), name='product-list'),
    path('blogposts/', BlogPostList.as_view(), name='blogpost-list'),



]
