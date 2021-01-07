from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string, get_template
from django.template import Context
from orders.models import Order
import weasyprint
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def order_email_task(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Order {order.order_id}"
    mail_body = render_to_string('email.html', context={'order': order})
    mail = EmailMessage(subject, mail_body, to=[order.email])
    mail.content_subtype = "html"                                      # This is very important to send as HTML
    # Generating PDF
    pdf_html = render_to_string('pdf.html', context={'order': order})
    empty = BytesIO()
    stylesheet = [weasyprint.CSS(settings.STATIC_CSS_DIR + 'pdf.css')]
    weasyprint.HTML(string=pdf_html).write_pdf(target=empty, stylesheets=stylesheet)
    mail.attach(f"Order {order.order_id}.pdf", empty.getvalue(), 'application/pdf')
    mail.send()