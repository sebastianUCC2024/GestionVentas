from django.db import models
from django.conf import settings
from clientes.models import Cliente


class OportunidadVenta(models.Model):

    ESTADO_CHOICES = [
        ('nueva', 'Nueva'),
        ('en_proceso', 'En proceso'),
        ('ganada', 'Ganada'),
        ('perdida', 'Perdida'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='oportunidades'
    )

    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas'
    )

    titulo = models.CharField(max_length=150)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='nueva'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_cierre_estimada = models.DateField(
        blank=True,
        null=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Oportunidad de Venta'
        verbose_name_plural = 'Oportunidades de Venta'

    def __str__(self):
        return f'{self.titulo} - {self.cliente.nombre}'


class Seguimiento(models.Model):

    TIPO_CONTACTO_CHOICES = [
        ('llamada', 'Llamada'),
        ('correo', 'Correo'),
        ('reunion', 'Reunión'),
        ('whatsapp', 'WhatsApp'),
        ('otro', 'Otro'),
    ]

    oportunidad = models.ForeignKey(
        OportunidadVenta,
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    tipo_contacto = models.CharField(
        max_length=20,
        choices=TIPO_CONTACTO_CHOICES
    )

    observaciones = models.TextField()

    fecha_contacto = models.DateTimeField(
        auto_now_add=True
    )

    proximo_contacto = models.DateField(
        blank=True,
        null=True
    )

    completado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_contacto']
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'

    def __str__(self):
        return f'{self.tipo_contacto} - {self.cliente.nombre}'