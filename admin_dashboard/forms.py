from django import forms
from products.models import Product
from categories.models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "stock",
            "is_available",
        ]

        widgets = {
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Name"
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "product-slug"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "image": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"