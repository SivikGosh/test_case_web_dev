from django import forms


class ReportForm(forms.Form):
    address = forms.CharField()
    date = forms.DateField(widget=forms.SelectDateWidget)
    income = forms.DecimalField()
