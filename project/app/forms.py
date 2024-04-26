from django import forms


class ReportForm(forms.Form):
    address = forms.CharField()
    income = forms.DecimalField()
