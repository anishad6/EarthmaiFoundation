from django import forms
from Earthmaiapp.models import Confirmorder  # Import the Donation model from models.py

class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Confirmorder
        # fields=["id","user","amount","message","date"]
        fields = ['amount', 'message']  # Fields to include in the form
