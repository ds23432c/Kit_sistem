from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['reg_number', 'brand', 'model', 'specs', 'quantity', 'equipment_type', 'room',
                  'condition', 'is_present', 'date_added', 'last_check_date', 'next_check_date', 'cost', 'photo']
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'last_check_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'next_check_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'specs': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }
        labels = {
            'reg_number': 'Регистрационный номер',
            'brand': 'Марка',
            'model': 'Модель',
            'specs': 'Технические характеристики',
            'quantity': 'Количество',
            'equipment_type': 'Вид оборудования',
            'room': 'Кабинет',
            'condition': 'Состояние',
            'is_present': 'На месте',
            'cost': 'Стоимость (руб.)',
        }
