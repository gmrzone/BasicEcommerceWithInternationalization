from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created_task(order_id):
    """
    Task to send e-mail notification to user when the order is sucessfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order ID: {order.order_id}"

    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.order_id}.'


    main_sent = send_mail(subject, message, 'saiyedafzal0@gmail.com', [order.email])

    return main_sent