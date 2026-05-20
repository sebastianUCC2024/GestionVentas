from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from clientes.models import Cliente
from ventas.models import OportunidadVenta


@login_required
def reporte_clientes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_clientes.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setTitle("Reporte de Clientes")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, "Reporte de Clientes")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 70, "Sistema GestionVentas CRM")

    y = height - 110

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(50, y, "Nombre")
    pdf.drawString(180, y, "Documento")
    pdf.drawString(280, y, "Correo")
    pdf.drawString(430, y, "Estado")

    y -= 20
    pdf.setFont("Helvetica", 8)

    clientes = Cliente.objects.all().order_by('nombre')

    for cliente in clientes:
        if y < 50:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 8)

        pdf.drawString(50, y, str(cliente.nombre)[:22])
        pdf.drawString(180, y, str(cliente.documento)[:18])
        pdf.drawString(280, y, str(cliente.correo)[:28])
        pdf.drawString(430, y, str(cliente.estado).title())

        y -= 18

    pdf.save()
    return response


@login_required
def reporte_ventas_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    headers = [
        "Título",
        "Cliente",
        "Vendedor",
        "Monto",
        "Estado",
        "Fecha creación",
        "Fecha cierre estimada",
    ]

    ws.append(headers)

    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    ventas = OportunidadVenta.objects.select_related('cliente', 'vendedor').all()

    for venta in ventas:
        ws.append([
            venta.titulo,
            venta.cliente.nombre,
            venta.vendedor.username if venta.vendedor else "Sin asignar",
            float(venta.monto),
            venta.get_estado_display(),
            venta.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
            venta.fecha_cierre_estimada.strftime("%d/%m/%Y") if venta.fecha_cierre_estimada else "No definida",
        ])

    for column_cells in ws.columns:
        length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 4

    wb.save(response)
    return response