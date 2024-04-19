from django import forms


class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)
    income = forms.DecimalField()
