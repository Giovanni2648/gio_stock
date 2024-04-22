from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django import forms
from django.forms import BaseFormSet, formset_factory, ModelChoiceField
#from django.forms import ModelForm, modelformset_factory
from .models import * 

#Categories Form
class CategoryForm(forms.ModelForm):
	class Meta:
		model = Categories
		fields = ['name']
		widgets={"name": forms.TextInput(attrs={'class': "form-control"})}

#Transactions Form
class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = '__all__'

#Products Forms
class ProductForm(forms.ModelForm):
	class Meta:
		model = Products
		exclude = ['total_price', 'total_cost']
		widgets={
			"name": forms.TextInput(attrs={'class': "form-control"}),
			"brand": forms.TextInput(attrs={'class': "form-control"}),
			"quantity": forms.NumberInput(attrs={'class': "form-control"}),
			"price": forms.NumberInput(attrs={'class': "form-control"}),
			"cost": forms.NumberInput(attrs={'class': "form-control"}),
			"category": forms.Select(attrs={'class': "form-control"}),
			"image": forms.ClearableFileInput(attrs={'class': "form-control"}),
		}  

class ProductsCategoryForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = ['category']
		widgets={
			"category": forms.Select(attrs={'class': "form-control"	}),
		
		}

class BaseCategoryFormSet(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return
		for form in self.forms:
			if self.can_delete and self._should_delete_form(form):
				continue
			category = form.cleaned_data.get("category")
			if category == None:
				raise ValidationError("Some Field is Empty")

class TotalProductForm(forms.Form):
	total = forms.IntegerField(label="Total In %", widget=forms.NumberInput(attrs={'class': "form-control"}))

class TotalByCategoryProductForm(ProductsCategoryForm):
	total = forms.IntegerField(label="Total In %", widget=forms.NumberInput(attrs={'class': "form-control"}))

#Suppliers Forms
class SupplierForm(forms.ModelForm):
	class Meta:
		model = Suppliers
		exclude = ['products']
		widgets={
			"image": forms.ClearableFileInput(attrs={'class': "form-control"}),
			"name": forms.TextInput(attrs={'class': "form-control"}),
			"description": forms.TextInput(attrs={'class': "form-control"}),
			"quantity": forms.NumberInput(attrs={'class': "form-control"}),
			"category": forms.Select(attrs={'class': "form-control"}),
			"review": forms.Select(attrs={'class': "form-control"}),
		}

class SuppliersCategoryForm(forms.ModelForm):
	class Meta:
		model = Suppliers
		fields = ['category']
		widgets={
			"category": forms.Select(attrs={'class': "form-control"	}),
		
		}

#Entries Forms
# class EntryForm(forms.ModelForm):
# 	class Meta:
# 		model = Entries
# 		fields = ['datetime' ,'supplier']
# 		widgets = {
# 			'datetime' : forms.DateInput(format="%d-%m-%y", attrs={"class" : 'form-control'}),
# 			'supplier' : forms.Select(attrs={"class" : 'form-control'}),
# 		}
# class EntryProductsForm(forms.ModelForm):
# 	class Meta:
# 		model = Entries
# 		fields = ['id', 'supplier']
# 		widgets = {
# 			'datetime' : forms.DateInput(format="%d-%m-%y", attrs={"class" : 'form-control'}),
# 			'supplier' : forms.Select(attrs={"class" : 'form-control'}),
# 		}

#Exits Forms
class ExitForm(forms.ModelForm):
	class Meta:
		model = Exits
		fields = '__all__'