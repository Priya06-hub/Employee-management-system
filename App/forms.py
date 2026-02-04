from django import forms
from .models import Employee
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class Emp_form(forms.ModelForm):
    class Meta:
        model = Employee
        fields="__all__"
        
class Emp_edit_form(forms.ModelForm):
    class Meta:
        model=Employee
        fields=['F_name','L_name','Email','Address','Contact_no']
