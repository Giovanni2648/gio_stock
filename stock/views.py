from django_htmx.http import HttpResponseClientRefresh, HttpResponseLocation, retarget
from django.core.paginator import Paginator
from stock.forms import BaseCategoryFormSet
from django.forms import formset_factory
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *

def index(request):
	context = None
	return render(request, 'stock/base_template.html')

#CRUD Products

def products(request):
	order = 'asc'
	value = request.POST.get('search')
	print(value)
	if value:
		products = Products.objects.filter(name__icontains=value)
	else:
		products = Products.objects.all()
	paginator = Paginator(products, 5)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		'order' : order,
		'products' : products,
		'page_obj' : page_obj,
	}
	return render(request, 'stock/products/products.html', context)

def create_product(request):
	product_form = ProductForm()
	products = Products()
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			category = Categories.objects.get(id=request.POST['category'])
			product_form.save(commit=False)
			products.image = request.FILES['image']
			products.name = request.POST['name']
			products.brand = request.POST['brand']
			products.cost = request.POST['cost']
			products.price = request.POST['price']
			products.quantity = request.POST['quantity']
			products.total_cost = int(request.POST['cost']) * int(request.POST['quantity'])
			products.total_price = int(request.POST['price']) * int(request.POST['quantity'])
			products.category = category
			products.save()
			return HttpResponseClientRefresh()
	context = {
		'form' : product_form,
	}
	return render(request, 'stock/products/create_product.html', context)

def update_product(request, pk):
	product = Products.objects.get(id=pk)
	product_form = ProductForm(instance=product)
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES, instance=product)
		if product_form.is_valid():
			category = Categories.objects.get(id=request.POST['category'])
			product_form.save(commit=False)
			if request.FILES:
				product.image = request.FILES['image']
			product.name = request.POST['name']
			product.cost = request.POST['cost']
			product.price = request.POST['price']
			product.quantity = request.POST['quantity']
			product.total_cost = int(request.POST['cost']) * int(request.POST['quantity'])
			product.total_price = int(request.POST['price']) * int(request.POST['quantity'])
			product.category = category
			product.save(force_update=True)
			return HttpResponseClientRefresh()
	context = {
		'form' : product_form,
		'pk' : pk
	}
	return render(request, 'stock/products/update_product.html', context)

def delete_product(request, pk):
	product = Products.objects.get(id=pk)
	product.delete()
	return HttpResponseClientRefresh()

def delete_products(request):
	order = 'asc'
	if request.method == "POST":
		products_list = request.POST.getlist('products[]')
		for products in products_list:	
			product = Products.objects.get(id=products)
			product.delete()
		return HttpResponseClientRefresh()
	products = Products.objects.all()
	context = {
		'products': products,
		'order' : order,
	}
	return render(request, 'stock/products/delete_products.html', context)

#Utilities Products

def modify_all_category_products(request):
	CategoryFormSet = formset_factory(ProductsCategoryForm, extra=2, formset=BaseCategoryFormSet)
	formset = CategoryFormSet() 
	if request.method == "POST":
		formset = CategoryFormSet(request.POST) 
		category1 = request.POST['form-0-category']
		category2 = request.POST['form-1-category']
		if formset.is_valid():
			products = Products.objects.filter(category=category1)
			category2 = Categories.objects.get(id=category2)
			for product in products:
				product.category = category2
				product.save()
			return HttpResponseClientRefresh()
	context = {
		'forms' : formset,
	}
	return render(request, 'stock/products/utilities/modify_all_category_products.html', context)

def modify_some_category_products(request):
	CategoryFormSet = formset_factory(ProductsCategoryForm, formset=BaseCategoryFormSet)
	formset = CategoryFormSet() 
	
	products = Products.objects.all()
	
	context = {
		'products' : products,
		'forms' : formset,
	}
	response = render(request, 'stock/products/utilities/modify_some_category_products.html', context)
	
	if request.method == "POST":
		products_list = request.POST.getlist('products[]')
		formset = CategoryFormSet(request.POST) 
		category = request.POST['form-0-category']
		if formset.is_valid():
			category = Categories.objects.get(id=category)
			for product in products_list:
				product = Products.objects.get(id=product)
				product.category = category
				product.save()
			return HttpResponseClientRefresh()
		else:
			context = {
				'products' : products,
				'forms' : formset,
			}
			response = render(request, 'stock/products/utilities/modify_some_category_products.html', context)
			retarget(response, 'body')
			return response
	return response

def increase_price(request, category):
	print(category)
	if category == "True":
		if request.method == "POST":
			form = TotalProductForm(request.POST)
			if form.is_valid():
				products = Products.objects.all()
				for product in products:
					product.total += int(product.total)*int(request.POST['total'])/100
					product.price = int(product.total) / int(product.quantity)
					product.save()
				return HttpResponseClientRefresh()
		form = TotalProductForm()
		context = {
			'form' : form,
			'category' : True
		}
		return render(request, 'stock/products/utilities/increase_price.html', context)
	else:
		if request.method == "POST":
			form = TotalByCategoryProductForm(request.POST)
			if form.is_valid():
				products = Products.objects.filter(category=request.POST['category'])
				for product in products:
					product.total += int(product.total)*int(request.POST['total'])/100
					product.price = int(product.total) / int(product.quantity)
					product.save()
				return HttpResponseClientRefresh()
		form = TotalByCategoryProductForm()
		context = {
			'form' : form,
			'category' : False
		}
		return render(request, 'stock/products/utilities/increase_price.html', context)
	return HttpResponse()

def products_filter(request, index, order , page, id):
	index = int(index)
	if index <= 5 and index >= 0:
		filter_dict = {
		0 : 'name',
		1 : 'brand',
		2 : 'price',
		3 : 'cost',
		4 : 'quantity',
		5 : 'category',
		}
		supplier = None
		filter_value = filter_dict[index]
		if order == 'asc':
			filter_value = f"-{filter_value}"
			order = 'desc'
		else:
			filter_value = filter_value.removeprefix('-')
			order = 'asc'
		if page == "supplier":
			supplier = Suppliers.objects.get(id=int(id))
			print(id, supplier)
			products = supplier.products.order_by(filter_value)
		else:
			products = Products.objects.order_by(filter_value)
		paginator = Paginator(products, 5)
		page_number = request.GET.get("page")
		page_obj = paginator.get_page(page_number)
		if page == "products":
			context = {
				'order' : order,
				'products' : products,
				'page_obj' : page_obj,
			}
			response = render(request, 'stock/products/products.html', context)
			retarget(response, 'body')
			return response

		if page == "delete_products":
			context = {
				'order' : order,
				'products' : products,	
			}
			response = render(request, 'stock/products/delete_products.html', context)
			retarget(response, '#main-container')
			return response
		if page == "supplier":
			context = {
				'order' : order,
				'supplier' : supplier,
				'products' : products,
				'page_obj' : page_obj,	
			}
			return render(request, 'stock/suppliers/supplier/table.html', context)

#CRUD Categories

def categories(request, error=None):
	categories = Categories.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		'categories' : categories,
		'page_obj' : page_obj,
		'error' : error,
	}
	return render(request, 'stock/categories/categories.html', context)

def create_category(request):
	category_form = CategoryForm()
	if request.method == 'POST':
		category_form = CategoryForm(request.POST)
		if category_form.is_valid():
			category_form.save()
			return HttpResponseClientRefresh()
	context = {
		'form' : category_form,
	}
	return render(request, 'stock/categories/create_category.html', context)

def update_category(request, pk):
	category = Categories.objects.get(id=pk)
	category_form = CategoryForm(instance=category)
	if request.method == 'POST':
		category_form = CategoryForm(request.POST, request.FILES, instance=category)
		if category_form.is_valid():
			category_form.save()
			return HttpResponseClientRefresh()
	context = {
		'form' : category_form,
		'pk' : pk
	}
	return render(request, 'stock/categories/update_category.html', context)

def delete_category(request, pk):
	try:
		category = Categories.objects.get(id=pk)
		category.delete()
		return HttpResponseClientRefresh()
	except models.RestrictedError as error:
		return HttpResponse(f"<h5 class=\"alert bg-danger\">Error: First Delete or Modify the Products Referenced to that Category</h5>")

def delete_categories(request):
	if request.method == "POST":
		categories_list = request.POST.getlist('categories[]')
		print(request.POST)
		print(categories_list)
		for categories in categories_list:	
			category = Categories.objects.get(id=categories)
			category.delete()
		return HttpResponseClientRefresh()
	categories = Categories.objects.all()
	context = {
		'categories': categories,
	}
	return render(request, 'stock/categories/delete_categories.html', context)


#Suppliers

def suppliers(request):
	order = "asc"
	value = request.POST.get('search')
	if value:
		supplier = Suppliers.objects.filter(name__icontains=value)
	else:
		supplier = Suppliers.objects.all()
	paginator = Paginator(supplier, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {
		'suppliers' : supplier,
		'page_obj' : page_obj,
		'order' : order,
	}
	return render(request, 'stock/suppliers/suppliers.html', context)

def create_supplier(request):
	supplier_form = SupplierForm()
	suppliers = Suppliers()
	if request.method == 'POST':
		supplier_form = SupplierForm(request.POST, request.FILES)
		if supplier_form.is_valid():
			category = Categories.objects.get(id=request.POST['category'])
			supplier_form.save(commit=False)
			suppliers.image = request.FILES['image']
			suppliers.name = request.POST['name']
			suppliers.description = request.POST['description']
			suppliers.category = category
			suppliers.review = request.POST['review']
			suppliers.save()
			return HttpResponseClientRefresh()
	context = {
		'form' : supplier_form,
	}
	return render(request, 'stock/suppliers/create_supplier.html', context)

def update_supplier(request, pk):
	supplier = Suppliers.objects.get(id=pk)
	supplier_form = SupplierForm(instance=supplier)
	if request.method == 'POST':
		supplier_form = SupplierForm(request.POST, request.FILES, instance=supplier)
		if supplier_form.is_valid():
			category = Categories.objects.get(id=request.POST['category'])
			supplier_form.save(commit=False)
			if request.FILES:
				supplier.image = request.FILES['image']
			supplier.name = request.POST['name']
			supplier.description = request.POST['description']
			supplier.category = category
			supplier.review = request.POST['review']
			supplier.save(force_update=True)
			return HttpResponseClientRefresh()
	context = {
		'form' : supplier_form,
		'pk' : pk
	}
	return render(request, 'stock/suppliers/update_supplier.html', context)

def delete_supplier(request, pk):
	supplier = Suppliers.objects.get(id=pk)
	supplier.delete()
	return HttpResponseClientRefresh()

def delete_suppliers(request):
	suppliers = Suppliers.objects.all()
	if request.method == "POST":
		suppliers_list = request.POST.getlist('suppliers[]')
		print(request.POST)
		print(suppliers_list)
		for supplier in suppliers_list:	
			supplier = Suppliers.objects.get(id=supplier)
			supplier.delete()
		return HttpResponseClientRefresh()
	context = {
		'suppliers': suppliers,
	}
	return render(request, 'stock/suppliers/delete_suppliers.html', context)

def modify_all_category_suppliers(request):
	CategoryFormSet = formset_factory(SuppliersCategoryForm, extra=2, formset=BaseCategoryFormSet)
	formset = CategoryFormSet() 
	if request.method == "POST":
		formset = CategoryFormSet(request.POST) 
		category1 = request.POST['form-0-category']
		category2 = request.POST['form-1-category']
		if formset.is_valid():
			suppliers = Suppliers.objects.filter(category=category1)
			category2 = Categories.objects.get(id=category2)
			for supplier in suppliers:
				supplier.category = category2
				supplier.save()
			return HttpResponseClientRefresh()
	context = {
		'forms' : formset,
	}
	return render(request, 'stock/suppliers/utilities/modify_all_category_suppliers.html', context)

def modify_some_category_suppliers(request):
	CategoryFormSet = formset_factory(SuppliersCategoryForm, formset=BaseCategoryFormSet)
	formset = CategoryFormSet() 
	
	suppliers = Suppliers.objects.all()
	
	context = {
		'suppliers' : suppliers,
		'forms' : formset,
	}
	response = render(request, 'stock/suppliers/utilities/modify_some_category_suppliers.html', context)
	
	if request.method == "POST":
		suppliers_list = request.POST.getlist('suppliers[]')
		formset = CategoryFormSet(request.POST) 
		category = request.POST['form-0-category']
		if formset.is_valid():
			category = Categories.objects.get(id=category)
			for supplier in suppliers_list:
				supplier = Suppliers.objects.get(id=supplier)
				supplier.category = category
				supplier.save()
			return HttpResponseClientRefresh()
		else:
			context = {
				'suppliers' : suppliers,
				'forms' : formset,
			}
			response = render(request, 'stock/suppliers/utilities/modify_some_category_suppliers.html', context)
			retarget(response, 'body')
			return response
	return response

def suppliers_filter(request, index, order, page):
	index = int(index)
	if index <= 5 and index >= 0:
		filter_dict = {
		0 : 'name',
		1 : 'category',
		2 : 'review',
		}
		filter_value = filter_dict[index]
		if order == 'asc':
			filter_value = f"-{filter_value}"
			order = 'desc'
		else:
			filter_value = filter_value.removeprefix('-')
			order = 'asc'
		suppliers = Suppliers.objects.order_by(filter_value)
		paginator = Paginator(suppliers, 5)
		page_number = request.GET.get("page")
		page_obj = paginator.get_page(page_number)
		if page == "suppliers":
			context = {
				'order' : order,
				'suppliers' : suppliers,
				'page_obj' : page_obj,
			}
			response = render(request, 'stock/suppliers/suppliers.html', context)
			retarget(response, 'body')
			return response

		if page == "delete_suppliers":
			context = {
				'order' : order,
				'suppliers' : suppliers,	
			}
			response = render(request, 'stock/suppliers/delete_products.html', context)
			retarget(response, '#main-container')
			return response

#Supplier Dashboard

def supplier_dashboard(request, pk):
	pk = int(pk)
	order = "asc"
	supplier = Suppliers.objects.get(id=pk)
	value = request.POST.get('search')
	if value:
		products = supplier.products.filter(name__icontains=value)
	else:
		products = supplier.products.all()
	paginator = Paginator(products, 3)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	print(supplier.id, type(supplier.id))
	context = {
		'supplier' : supplier,
		'page_obj' : page_obj,
		'pk' : pk,
		'order' : order,
	}
	return render(request, 'stock/suppliers/supplier/supplier_dashboard.html', context)

def create_product_supplier(request, pk):
	product_form = ProductForm()
	products = Products()
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			category = Categories.objects.get(id=request.POST['category'])
			supplier = Suppliers.objects.get(id=pk)
			product = supplier.products.create(
				image = request.FILES['image'],
				name = request.POST['name'],
				quantity = request.POST['quantity'],
				price = request.POST['price'],
				cost = request.POST['cost'],
				total_price = int(request.POST['price']) * int(request.POST['quantity']),
				total_cost = int(request.POST['cost']) * int(request.POST['quantity']), 
				category = category)
			return HttpResponseClientRefresh()
	context = {
		'form' : product_form,
		'pk' : pk,
	}
	return render(request, 'stock/suppliers/supplier/utilities/create_product_supplier.html', context)

def add_products_supplier(request, pk):
	products  = Products.objects.all()
	supplier = Suppliers.objects.get(id=pk)
	if request.method == "POST":
		products = request.POST.getlist('products[]')
		if products:
			for product in products:
				supplier.products.add(product)
			return HttpResponseClientRefresh()
		else:
			print("form invalid")

	paginator = Paginator(products, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'products' : products,
		'page_obj' : page_obj,
		'pk' : pk
	}
	return render(request, "stock/suppliers/supplier/utilities/add_products.html", context)

def delete_product_supplier(request, pk, pk_product):
	print(pk, pk_product)
	supplier = Suppliers.objects.get(id=pk)
	product = Products.objects.get(id=pk_product)
	remover = supplier.products.remove(product)
	return HttpResponseClientRefresh()

def delete_products_supplier(request, pk):
	if request.method == "POST":
		supplier = Suppliers.objects.get(id=pk)
		products = request.POST.getlist('products[]')
		for product in products:
			product = supplier.products.remove(product)
		return HttpResponseClientRefresh()
	supplier = Suppliers.objects.get(id=pk)
	products = supplier.products.all()
	context = {
		'supplier' : supplier,
		'products' : products,
		'pk' : pk,
	}
	return render(request, 'stock/suppliers/supplier/utilities/delete_products.html', context)

#Entries

def entries(request):
	entries = Entries.objects.all()
	print(entries)
	paginator  = Paginator(entries, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		#'products' : products,
		'page_obj' : page_obj,
		'entries' : entries,
	}
	return render(request, 'stock/entries/entries.html', context)

def create_entry(request):
	#crear un formulario que contenga cantidad y el checkbox y utilizar un formset para mostrarlo en cada producto.
	form = EntryForm()
	products = Products.objects.all()
	paginator = Paginator(products, 4)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	print(request.POST)
	if request.method == "POST":
		form = EntryForm(request.POST)
		if form.is_valid():
			print(request.POST)
			return HttpResponse("Is Valid")
		else:
			print(request.POST)
	context = {
		'form' : form,
		'products' : products,
		'page_obj' : page_obj,
	}
	return render(request, 'stock/entries/create_entry.html', context)

def update_entry(request):
	pass

def delete_entry(request):
	pass

def delete_entries(request):
	pass