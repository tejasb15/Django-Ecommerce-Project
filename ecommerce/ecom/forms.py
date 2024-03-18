from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User


class category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['catname']

    
class subcategory_form(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}),initial='')

    def __init__(self, *args, **kwargs):
        super(subcategory_form, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

        # Add a disabled option to the queryset with the empty label
        choices = self.fields['category'].widget.choices
        choices = [("", "Select your category")] + list(choices)
        self.fields['category'].widget.choices = choices

class product_form(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    specification = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = '__all__'

    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), label='SubCategory', empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}),initial='')

    def __init__(self, *args, **kwargs):
        super(product_form, self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.all()

        choices = self.fields['subcategory'].widget.choices
        choices = [("", "Select your Sub Category")] + list(choices)
        self.fields['subcategory'].widget.choices = choices


class productimage_form(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ['user']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = [('', 'Select your gender')] + list(self.fields['gender'].choices)[1:]


class Address_form(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        fields = ['customer_name', 'phone', 'street', 'landmark','city', 'state','country','pincode','alt_phone']