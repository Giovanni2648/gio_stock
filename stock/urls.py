from django.urls import path, include
from stock.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name='stock'
urlpatterns = [
	path('', index, name="index"),

	#Products
	path('products-dashboard/',
		include([
			#CRUD
			path('',products, name="products"),
			path('create-product/', create_product, name="create_product"),
			path('update-product/<pk>/', update_product, name="update_product"),
			path('delete-product/<pk>/', delete_product, name="delete_product"),
			path('delete-products/', delete_products, name="delete_products"),
			
			#Products Utilities
			path('modify-all-category-products/', modify_all_category_products, name="modify_all_category_products"),
			path('modify-some-category-products/', modify_some_category_products, name="modify_some_category_products"),
			path('increase-price/<category>/', increase_price, name="increase_price"),
			path('products_filter/<index>/<order>/<page>/', products_filter, name="products_filter"),
			path('search-products/', search_products, name="search_products"),
			])),
	
	#Categories
	path('categories-dashboard/',
		include([
			#CRUD
			path('',  categories, name="categories"),
			path('create-category/', create_category, name="create_category"),
			path('update-category/<pk>/', update_category, name="update_category"),
			path('delete-category/<pk>/', delete_category, name="delete_category"),
			path('delete-categories/', delete_categories, name="delete_categories"),
		])),

	#Suppliers
	path('suppliers-dashboard/', 
		include([
			#CRUD
			path('',suppliers, name="suppliers"),
			path('create-supplier/', create_supplier, name="create_supplier"),
			path('update-supplier/<pk>/', update_supplier, name="update_supplier"),
			path('delete-supplier/<pk>/', delete_supplier, name="delete_supplier"),
			path('delete-suppliers/', delete_suppliers, name="delete_suppliers"),

			#Suppliers Utilities
			path('modify-all-category-suppliers/', modify_all_category_suppliers, name="modify_all_category_suppliers"),
			path('modify-some-category-suppliers/', modify_some_category_suppliers, name="modify_some_category_suppliers"),
			path('suppliers-filter/<index>/<order>/<page>', suppliers_filter, name="suppliers_filter"),

		])),
	
	path('supplier-dashboard/<int:pk>/',
		include([
			#Supplier Dashboard
		    path('',  supplier_dashboard, name="supplier"),
		    path('create-product/<int:pk>/', create_product_supplier, name="create_product_supplier"),
			path('add-product-supplier/<int:pk>/', add_products_supplier, name="add_products_supplier"),
			path('delete-product-supplier/<int:pk_product>/<int:pk_supplier>/', delete_product_supplier, name="delete_product_supplier"),
			path('delete-products-supplier/<int:pk>/', delete_products_supplier, name="delete_products_supplier"),
		])),
	    
    path('entries-dashboard/',
    	include([
		    path('', entries, name="entries"),
		    path('create-entry/', create_entry, name="create_entry"),
		    path('update-entry/<pk>/', update_entry, name="update_entry"),
		    path('delete-entry/<pk>/', delete_entry, name="delete_entry"),
		    path('delete-entries/', delete_entries, name="delete_entries"),
		])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)