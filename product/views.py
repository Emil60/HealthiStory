from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import MobileHealthStationOrderForm, SymptomCheckOrderForm
from . import services
from django.contrib import messages
from django.utils.translation import gettext
from django.utils import translation


def list_products_view(request):
    """return list of products"""
    model1 = Product.objects.filter(language=translation.get_language())
    model2 = Category.objects.filter(language=translation.get_language())
    return render(request, 'product/products.html', {"categories": model2, "products": model1})


def categorized(request, category_code):
    """return list of categorised products"""
    model1 = Product.objects.filter(category__category_code=category_code, language=translation.get_language())
    model2 = Category.objects.filter(language=translation.get_language())
    return render(request, "product/products.html", {"categories": model2, "products": model1})


def single_product_view(request, product_code):
    """return single product and form for order with email notification"""
    form = MobileHealthStationOrderForm()
    if product_code == 'Mobile_Medi-Lab':
        form = MobileHealthStationOrderForm()
    elif product_code == 'sc':
        form = SymptomCheckOrderForm()
    model1 = Product.objects.get(product_code=product_code, language=translation.get_language())
    if request.method == "POST":
        if product_code == 'Mobile_Medi-Lab':
            form = MobileHealthStationOrderForm(request.POST)
            if form.is_valid():
                form_data = form.clean()
                if services.mobile_station_order_send_mail(**form_data):
                    output = gettext("""<div class="alert alert-success alert-dismissable text-center">
                                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                    We received your messages and will come back to you as soon as possible.
                                    </div>""")
                    messages.success(request, output)
                else:
                    output = gettext("""<div class="alert alert-danger alert-dismissable text-center">
                                                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                                ERROR: Please fill at least one field in \"Quantity of products\"
                                                </div>""")
                    messages.success(request, output)
                return render(request, "product/single_product.html",
                              {"product": model1, "form": form, "product_code": product_code})
            else:
                output = gettext("""<div class="alert alert-danger alert-dismissable text-center">
                                                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                                    ERROR: Please fill the mandatory fields in the \"Order Now\" form!
                                                    </div>""")
                messages.success(request, output)
                return render(request, "product/single_product.html", {"product": model1, "form": form, "product_code": product_code})
        elif product_code == 'sc':
            form = SymptomCheckOrderForm(request.POST)
            if form.is_valid():
                form_data = form.clean()
                if services.symptom_check_order_send_mail(**form_data):
                    output = gettext("""<div class="alert alert-success alert-dismissable text-center">
                                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                    We received your messages and will come back to you as soon as possible.
                                    </div>""")
                    messages.success(request, output)
                return render(request, "product/single_product.html",
                              {"product": model1, "form": form, "product_code": product_code})
            else:
                output = gettext("""<div class="alert alert-danger alert-dismissable text-center">
                                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                    ERROR: Please fill the mandatory fields in the \"Order Now\" form!
                                    </div>""")
                messages.success(request, output)
                return render(request, "product/single_product.html", {"product": model1, "form": form, "product_code": product_code})
    else:
        return render(request, "product/single_product.html", {"product": model1, "form": form, "product_code": product_code})