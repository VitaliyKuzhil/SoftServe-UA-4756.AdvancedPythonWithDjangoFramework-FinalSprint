from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from order.forms import CreateAnOrderForm
from order.models import Order
from book.models import Book
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.contrib import messages
from order.constants import LOAN_PERIOD


@login_required
def create_an_order(request):
    if request.user.is_staff:
        messages.error(request, "Librarians can't create orders")
        return render(request, '403.html', status=403)
    
    # if request.method == 'POST':
    #     book_id = request.POST.get('book')

    #     book = get_object_or_404(Book, id=book_id)

    #     plated_end_at = timezone.now() + LOAN_PERIOD

    #     order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)

    #     if order is None:
    #         books = Book.objects.all()

    #         return render(request, 'order/create_an_order.html', {'error': 'No copies available.', 'books': books})

    #     return redirect('user_orders', user_id=request.user.id)

    # books = Book.objects.all()
    # return render(request, 'order/create_an_order.html', {'books': books})

    if request.method == 'POST':
        form = CreateAnOrderForm(request.POST, request=request)
    
        if form.is_valid():
            form.save()

            messages.success(request, "The new order successfully created!")
            return redirect('user_orders', user_id=request.user.id)
    else:
        form = CreateAnOrderForm(request=request)
    
    context = {'form': form}
    
    return render(request, 'order/create_an_order.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def status_an_order(request, order_id):

    try:
        order = Order.get_by_id(order_id)

    except Order.DoesNotExist:
        raise Http404("Order not found")

    if request.method == 'POST':
        order.change_order_status()
        return redirect('list_of_orders')

    return render(request, 'order/status_an_order.html', {'order': order})


@login_required
def user_orders(request, user_id):
    if not request.user.is_staff and request.user.id != user_id:
        messages.error(request, "Not allowed")
        return render(request, '403.html', status=403)

    if request.user.is_staff:
        return redirect(f"/orders/?user={user_id}")

    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'order/user_orders.html', {'orders': orders, 'user_id': user_id})


@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_orders(request):
    orders = Order.objects.all()
    user_id = request.GET.get('user')
    if user_id:
        orders = orders.filter(user_id=user_id)
    return render(request, 'order/list_of_orders.html', {'orders': orders, 'filtered_user_id': user_id})
