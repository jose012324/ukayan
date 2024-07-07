from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth. decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomLoginForm, SupplyForm, OutgoingStockForm, CashierReportForm, ReportDetailForm
from .models import Supply,Cashier,Report,Product,OldStock,CustomUser
from django.db.models import Sum


def logout_view(request):
    logout(request)
    return redirect('login')

def loading(request):
    logout(request)
    return redirect('login')

@login_required
def loading_view(request):
    return render(request, 'loading.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('staff_dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Wrong username or password'})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    
    total_products = Supply.objects.count()
    total_quantity = Supply.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_users = CustomUser.objects.count()
    total_sale = Report.objects.aggregate(Sum('sale'))['sale__sum'] or 0
    
    return render(request, 'admin_dashboard.html', {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_users': total_users,
        'total_sale': total_sale
        
    })

@login_required
def view_staff(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request, 'view_staff.html', {'users': users})

@login_required
def add_supply(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    if request.method == 'POST':
        form  = SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SupplyForm()
    return render(request, 'add_supply.html', {'form': form})
    
@login_required
def outgoing_stock(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    if request.method == 'POST':
        form = OutgoingStockForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
                return redirect('admin_dashboard')
            else:
                form.add_error('quantity', 'Not enough stock available')
    else:
        form = OutgoingStockForm()
    return render(request, 'outgoing_stock.html', {'form': form})

@login_required
def view_stock(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    supplies = Supply.objects.all()
    if request.method == 'POST':
        supplies = Supply.objects.all()
        for supply in supplies:
            OldStock.objects.create(
                name=supply.name,
                quantity=supply.quantity,
                price=supply.price,
                display=supply.display
                )
        Supply.objects.all().delete()
        return redirect('view_oldstock')
    return render(request, 'view_stock.html', {'supplies': supplies})

@login_required
def view_oldstock(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')
    
    old_stocks = OldStock.objects.all()
    return render(request, 'view_oldstock.html', {'old_stocks': old_stocks})


@login_required
def view_report(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')

    cashiers = Cashier.objects.all()
    cashier_reports = []
    total_sale = Report.objects.all()

    for cashier in cashiers:
        reports = Report.objects.filter(cashier=cashier)
        if reports.exists():
            total_sale = reports.aggregate(Sum('sale'))['sale__sum'] or 0
            cashier_reports.append({
                'cashier': cashier,
                'reports': reports,
                'total_sale': total_sale
            })

    return render(request, 'view_report.html', {
        'cashier_reports': cashier_reports,
        'total_sale': total_sale
    })


@login_required
def staff_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        form = CashierReportForm(request.POST)
        if form.is_valid():
            cashier = form.save()
            request.session['cashier_id'] = cashier.id
            return redirect('report')
    else:
        form = CashierReportForm()
    return render(request, 'staff_dashboard.html', {'form': form})

@login_required
def report(request):
    if 'cashier_id' not in request.session:
        return redirect('staff_dashboard')
    cashier_id = request.session['cashier_id']
    cashier = get_object_or_404(Cashier, id=cashier_id)

    if request.method == 'POST':
        form = ReportDetailForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.cashier = cashier
            supply = get_object_or_404(Supply, id=product.product_name.id)
            if supply.quantity >= product.quantity:
                supply.quantity -= product.quantity
                supply.save()
                product.save()
                form = ReportDetailForm()
                return render(request, 'report.html', {'form': form, 'success': 'Report detail sent successfully!'})
            else:
                form.add_error('quantity', 'Not enough stock available')

    else:
        form = ReportDetailForm()
    return render(request, 'report.html', {'form': form})
@login_required
def view_table(request):
    if 'cashier_id' not in request.session:
        return redirect('staff_dashboard')
    cashier_id = request.session['cashier_id']
    cashier = get_object_or_404(Cashier, id=cashier_id)
    products = Product.objects.filter(cashier=cashier)
    
    total_sale = sum(product.sale for product in products)

    if request.method == "POST":
        for product in products:
            Report.objects.create(
                cashier=cashier,
                product_name=product.product_name,
                quantity=product.quantity,
                price=product.price,
                display=product.display,
                expenses=product.expenses,
                sale=product.sale
            )
        return redirect('loading_view')
    
    return render(request, 'view_table.html', {
        'cashier': cashier,
        'products': products,
        'total_sale': total_sale
    })