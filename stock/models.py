from django.db import models
from django.conf import settings

class Categories(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

class Products(models.Model):
	name = models.CharField(max_length=100)
	brand = models.CharField(max_length=100)
	quantity = models.IntegerField()
	price = models.IntegerField()
	cost = models.IntegerField()
	total_price = models.IntegerField()
	total_cost = models.IntegerField()
	image = models.ImageField(upload_to="products/")
	category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=True, blank=False)
	
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Product"
		verbose_name_plural = "Products"
		#ordering = ['image', 'name', 'quantity', 'price', 'category']

class Transactions(models.Model):
	transaction_choices = {
		'buy' : 'buy',
		'sell' : 'sell',
	}
	transacction_type = models.CharField(max_length=100, choices=transaction_choices)

	def __str__(self):
		return f"#{self.id} - {self.transacction_type}"

class Suppliers(models.Model):
	choices = {
		1 : 1,
		2 : 2,
		3 : 3,
		4 : 4,
		5 : 5
	}
	image = models.ImageField(upload_to="suppliers/")
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=True)
	review = models.IntegerField(choices=choices)
	products = models.ManyToManyField(Products)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Supplier"
		verbose_name_plural = "Suppliers"

class Entries(models.Model):
	datetime = models.DateField(blank=True)
	transaction = models.ForeignKey(Transactions, on_delete=models.DO_NOTHING)
	total = models.IntegerField(blank=True)

	def __str__(self):
		return f"{self.datetime} - {self.total}"

	class Meta:
		verbose_name = "Entries"
		verbose_name_plural = "Entries"

class Entry(models.Model):
	products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()
	cost = models.IntegerField()
	supplier = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, null=True)
	entry_code = models.ForeignKey(Entries, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f"{self.id}"

	class Meta:
		verbose_name = "Entry"
		verbose_name_plural = "Entry"

class Exits(models.Model):
	datetime = models.DateField(blank=True)
	transaction = models.ForeignKey(Transactions, on_delete=models.DO_NOTHING)
	total = models.IntegerField(blank=True)

	def __str__(self):
		return f"{self.datetime} - {self.total}"

	class Meta:
		verbose_name = "Exits"
		verbose_name_plural = "Exits"

class Exit(models.Model):
	products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()
	price = models.IntegerField()
	exit_code = models.ForeignKey(Exits, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f"{self.id}"

	class Meta:
		verbose_name = "Exit"
		verbose_name_plural = "Exit"
# class Pivot_Products_Supplier(models.Model):
# 	fk_product = models.ForeignKey('Products', on_delete=models.CASCADE)
# 	fk_supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return f"{self.fk_product} - {self.fk_supplier}"