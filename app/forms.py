from django import forms


class ReportForm(forms.Form):
    date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form_date'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_address'})
    )
    income = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form_income'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Дата'
        self.fields['address'].label = 'Адрес'
        self.fields['income'].label = 'Выручка'
