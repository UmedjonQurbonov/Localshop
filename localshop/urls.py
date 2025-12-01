from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, DeletedProductListView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('deleted/', DeletedProductListView.as_view(), name='deleted_list')
]
