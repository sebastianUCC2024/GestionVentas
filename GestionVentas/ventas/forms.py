from django import forms
from .models import OportunidadVenta, Pedido, Seguimiento


class OportunidadVentaForm(forms.ModelForm):
    class Meta:
        model = OportunidadVenta
        fields = [
            'cliente',
            'vendedor',
            'titulo',
            'descripcion',
            'monto',
            'estado',
            'fecha_cierre_estimada',
        ]

        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-control'}),
            'vendedor': forms.Select(attrs={'class': 'input-control'}),
            'titulo': forms.TextInput(attrs={
                'class': 'input-control',
                'placeholder': 'Ej: Venta de software CRM'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'input-control',
                'rows': 4,
                'placeholder': 'Describe la oportunidad de venta'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'input-control',
                'placeholder': 'Ej: 1500000'
            }),
            'estado': forms.Select(attrs={'class': 'input-control'}),
            'fecha_cierre_estimada': forms.DateInput(attrs={
                'class': 'input-control',
                'type': 'date'
            }),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        if monto is not None and monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')

        return monto


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = [
            'oportunidad',
            'cliente',
            'usuario',
            'tipo_contacto',
            'observaciones',
            'proximo_contacto',
            'completado',
        ]

        widgets = {
            'oportunidad': forms.Select(attrs={'class': 'input-control'}),
            'cliente': forms.Select(attrs={'class': 'input-control'}),
            'usuario': forms.Select(attrs={'class': 'input-control'}),
            'tipo_contacto': forms.Select(attrs={'class': 'input-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'input-control',
                'rows': 4,
                'placeholder': 'Escribe las observaciones del contacto'
            }),
            'proximo_contacto': forms.DateInput(attrs={
                'class': 'input-control',
                'type': 'date'
            }),
            'completado': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }
class PedidoForm(forms.ModelForm):
 class Meta:
        model = Pedido
        fields = ['producto', 'descripcion', 'cantidad']

        widgets = {
            'producto': forms.TextInput(attrs={
                'placeholder': 'Ej: Página web, sistema, diseño, asesoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Describe detalladamente lo que necesitas',
                'rows': 5
            }),
            'cantidad': forms.NumberInput(attrs={
                'min': 1
            }),
        }


class PedidoEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']