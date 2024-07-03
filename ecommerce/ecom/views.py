import requests
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages 
from django.db.models import Subquery, OuterRef ,Count, Q
from django.db.models.functions import Random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash,get_user_model
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm, SetPasswordForm
from django.core.paginator import Paginator
from datetime import date,timedelta,datetime
import uuid
import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Create your views here.

def userpublic_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/userindex/')
    else:
        category, subcategory, randsubcat = usernav_view(request)

        recent_products = Product.objects.order_by('-date')[:12]

        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'recent_products':recent_products,
        }

        return render(request,'user/userbase.html',context)

def usernav_view(request):
    category = Category.objects.all().order_by('id')
    subcategory = Subcategory.objects.all()
    randsubcat = Subcategory.objects.annotate(
        random_order=Random(),
        product_count=Count('product')
    ).order_by('category_id', 'random_order')[:12]



    return category, subcategory, randsubcat

def userindex_view(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        count_cart = Cart.objects.filter(user_id=request.user).count()
        

        recent_products = Product.objects.order_by('-date')[:12]


        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'recent_products':recent_products,
            'count_cart':count_cart,
        }
        return render(request,'user/userindex.html',context)
    else:
        return HttpResponseRedirect('/')

def shop_view(request,pk):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        count_cart = Cart.objects.filter(user_id=request.user).count()
        
        
        
        subcategory_filter = get_object_or_404(Subcategory, id=pk)
        products = Product.objects.filter(subcategory=subcategory_filter)


        paginator = Paginator(products,4)
        page_number = request.GET.get('page')
        productsfinal = paginator.get_page(page_number)


        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
            'products':products,
            'productsfinal':productsfinal,
            'subcategory_filter':subcategory_filter,
        }
        return render(request,'user/shop.html',context)
    else:
        return HttpResponseRedirect('/')

def contact(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)
        
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        count_cart = Cart.objects.filter(user_id=request.user).count()


        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('desc')

            mail_from = user.email
            mail_to = settings.EMAIL_HOST_USER
            send_mail(
                f"Subject: {subject}",
                f"From: {name} <{email}>\n\n{message}",
                mail_from,
                [mail_to],
                fail_silently=False,
            )

            messages.success(request, 'Message sent successfully.')
            return HttpResponseRedirect('/contact/')




        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
        }

        return render(request,'user/contact.html',context)
    else:
        return HttpResponseRedirect('/')
def detail(request,pk):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        product = Product.objects.get(id=pk)
        images = ProductImage.objects.filter(product=product)
        
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)


        count_cart = Cart.objects.filter(user_id=request.user).count()

        context = {
            'product':product,
            'images':images,
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
        }
        return render(request,'user/detail.html',context) 
    else:
        return HttpResponseRedirect('/')




def address_view(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        addresses=Address.objects.filter(user_id=request.user)

        count_cart = Cart.objects.filter(user_id=request.user).count()

        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'addresses':addresses,
            'count_cart':count_cart,
        }

        return render(request,'user/address.html',context) 
    else:
        return HttpResponseRedirect('/')


def Add_Address(request):
    if request.user.is_authenticated:

        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        if request.method == 'POST':
            AddressForm = Address_form(request.POST)
            if AddressForm.is_valid():
                address_instance = AddressForm.save(commit=False)
                address_instance.user = user
                address_instance.save() 
                messages.success(request, 'Address Added successfully.')
                return HttpResponseRedirect('/address/')
        else:
            AddressForm = Address_form()

        addresses=Address.objects.filter(user_id=request.user)

        count_cart = Cart.objects.filter(user_id=request.user).count()

        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'AddressForm':AddressForm,
            'addresses':addresses,
            'count_cart':count_cart,
        }

        return render(request,'user/add-address.html',context) 
    else:
        return HttpResponseRedirect('/')

def Edit_Address(request, pk):
    if request.user.is_authenticated:

        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        
        address = get_object_or_404(Address, id=pk)

        if address.user_id != request.user.id:
            return HttpResponseRedirect('/address/')

        addresses = Address.objects.filter(user_id=request.user).exclude(id=pk)
        
        if request.method == 'POST':
            AddressForm = Address_form(request.POST, instance=address)
            if AddressForm.is_valid():
                AddressForm.save()
                messages.success(request, 'Address updated successfully.')
                return HttpResponseRedirect('/address/')
        else:
            AddressForm = Address_form(instance=address)

        count_cart = Cart.objects.filter(user_id=request.user).count()

        context={
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'AddressForm': AddressForm,
            'address': address,
            'addresses':addresses,
            'count_cart':count_cart,
        }
        
        return render(request, 'user/edit-address.html',context)
    else:
        return HttpResponseRedirect('/')

def Delete_Address(request, pk):
    if request.user.is_authenticated:
        address = get_object_or_404(Address, id=pk)
        if address.user_id == request.user.id:
            address.delete()
            messages.success(request, 'Address deleted successfully.')
            return HttpResponseRedirect('/address/')
        else:
            return HttpResponseRedirect('/address/')
    else:
        return HttpResponseRedirect('/')


def checkout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_address_id = request.POST.get('selected_address_id')
            payment_method = request.POST.get('payment_method')
            address = Address.objects.get(pk=selected_address_id)

            date1 = datetime.now()
            datef = date1.strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4().hex)[:6:]
            order_id = f'MS{datef}-{unique_id}'

            order = Order.objects.create(order_id=order_id,user=request.user, address=address, status='Pending')

            cart_items = Cart.objects.filter(user_id=request.user)
            count_cart = Cart.objects.filter(user_id=request.user).count()

            total_cart_amount = 0 

            for item in cart_items:
                item.total_amount = item.quantity * item.product.price
                total_cart_amount += item.total_amount


            shipping_charge = 0
            if total_cart_amount  >= 100000:
                shipping_charge += 0
            elif total_cart_amount >= 20000:
                shipping_charge += 40
            elif total_cart_amount >= 10000:
                shipping_charge += 70
            elif total_cart_amount >= 100:
                shipping_charge += 120
            else:
                shipping_charge += 0

            discount = 0
            if count_cart >= 2:
                if total_cart_amount >= 1000:
                    # Apply 10% discount if both conditions are met
                    discount += 0.1 * total_cart_amount  
                else:
                    # Apply 5% discount if count is high but amount is less than $1000
                    discount += 0.05 * total_cart_amount  
            elif total_cart_amount >= 1000:
                # Apply $100 discount if count is less than 5 but amount is $1000 or more
                discount += 100

            total_amount = total_cart_amount - discount
            total_amount_pay = shipping_charge + total_amount

            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
                

            if payment_method == 'razorpay':
                return HttpResponseRedirect('/payment/')
                
            elif payment_method == 'cod':
                order.status = 'Order Confirmed'
                order.save()
                return HttpResponseRedirect('/order_confirm/')


            return HttpResponseRedirect('/order_confirm/')  # Redirect to order confirmation page
        else:

            category, subcategory, randsubcat = usernav_view(request)

            user = User.objects.get(id=request.user.id)
            user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

            count_cart = Cart.objects.filter(user_id=request.user).count()

            cart_items = Cart.objects.filter(user_id=user.id)

            total_cart_amount = 0 

            for item in cart_items:
                item.total_amount = item.quantity * item.product.price
                total_cart_amount += item.total_amount


            shipping_charge = 0
            if total_cart_amount  >= 100000:
                shipping_charge += 0
            elif total_cart_amount >= 20000:
                shipping_charge += 40
            elif total_cart_amount >= 10000:
                shipping_charge += 70
            elif total_cart_amount >= 100:
                shipping_charge += 120
            else:
                shipping_charge += 0

            discount = 0
            if count_cart >= 2:
                if total_cart_amount >= 1000:
                    # Apply 10% discount if both conditions are met
                    discount += 0.1 * total_cart_amount  
                else:
                    # Apply 5% discount if count is high but amount is less than $1000
                    discount += 0.05 * total_cart_amount  
            elif total_cart_amount >= 1000:
                # Apply $100 discount if count is less than 5 but amount is $1000 or more
                discount += 100

            total_amount = total_cart_amount - discount
            total_amount_pay = shipping_charge + total_amount

            addresses=Address.objects.filter(user_id=user.id)


            context = {
                'category':category,
                'subcategory':subcategory,
                'randsubcat':randsubcat,
                'user':user,
                'userprofile':user_profile,
                'count_cart':count_cart,
                'cart_items':cart_items,
                'addresses':addresses,
                'total_cart_amount':total_cart_amount,
                'count_cart':count_cart,
                'total_amount_pay':total_amount_pay,
                'shipping_charge':shipping_charge,
                'discount':discount,
                'total_amount':total_amount,
            }

            return render(request, 'user/checkout.html', context)
    else:
        return HttpResponseRedirect('/')


def Payment(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        count_cart = Cart.objects.filter(user_id=request.user).count()


        cart_items = Cart.objects.filter(user_id=request.user)

        total_cart_amount = 0 

        for item in cart_items:
            item.total_amount = item.quantity * item.product.price
            total_cart_amount += item.total_amount


        shipping_charge = 0
        if total_cart_amount  >= 100000:
            shipping_charge += 0
        elif total_cart_amount >= 20000:
            shipping_charge += 40
        elif total_cart_amount >= 10000:
            shipping_charge += 70
        elif total_cart_amount >= 100:
            shipping_charge += 120
        else:
            shipping_charge += 0

        discount = 0
        if count_cart >= 2:
            if total_cart_amount >= 1000:
                # Apply 10% discount if both conditions are met
                discount += 0.1 * total_cart_amount  
            else:
                # Apply 5% discount if count is high but amount is less than $1000
                discount += 0.05 * total_cart_amount  
        elif total_cart_amount >= 1000:
            # Apply $100 discount if count is less than 5 but amount is $1000 or more
            discount += 100

        total_amount = total_cart_amount - discount
        total_amount_pay = (shipping_charge + total_amount) 

        client = razorpay.Client(auth=("rzp_test_93atKPgF1eLJ4M", "ZighzyBxP2GddO81jA8fXqCy"))

    
        data = { "amount": {total_amount_pay}, "currency": "INR", "receipt": "order_rcptid_11" }
        
        order = Order.objects.filter(user=request.user, status='Pending')
        
        order.update(status='Order Confirmed')


    
        order_item = Order.objects.filter(user_id=request.user).order_by('-id').first()
        address = Address.objects.get(pk=order_item.address_id)

        Cart.objects.filter(user=request.user).delete()


        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
            'cart_items':cart_items,
            'total_cart_amount':total_cart_amount,
            'count_cart':count_cart,
            'address':address,
            'total_amount_pay':total_amount_pay*100,
            'callbackurl': "http://" + "127.0.0.1:8000" + "/order_confirm/"
        }
        return render(request,'user/payment.html',context)
    else:
        return HttpResponseRedirect('/')

def Cancel_Payment(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)
        user = User.objects.get(id=request.user.id)

        order_item = Order.objects.filter(user_id=request.user).order_by('-id').first()
        order_item.delete()

        return HttpResponseRedirect('/userindex/')

    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def Order_Confirm(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        order = Order.objects.filter(user=request.user, status='Pending')

        order.update(status='Order Confirmed')


        Cart.objects.filter(user=request.user).delete()

        lastorder = Order.objects.filter(user_id=request.user).order_by('-id').first()

        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'lastorder':lastorder
        }
        return render(request,'user/confirmation.html',context)
    else:
        return HttpResponseRedirect('/')



def myorder_view(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)
        count_cart = Cart.objects.filter(user_id=request.user).count()

        orders = Order.objects.filter(user=request.user).order_by('-odatetime')
        data = []
        for order in orders:
            items = OrderItem.objects.filter(order=order) 
            order_data = {
                'order': order,
                'address': order.address,
                'items': items,
            }
            data.append(order_data)
        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
            'data': data,
        }
        return render(request,'user/myorder.html',context)
    else:
        return HttpResponseRedirect('/')


def Search_View(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)
        count_cart = Cart.objects.filter(user_id=request.user).count()

        sdata = []
        if request.method == 'POST':
            search = request.POST.get('search')
            sdata = Product.objects.filter(Q(productname__icontains=search) | 
                                           Q(specification__icontains=search) | 
                                           Q(price__icontains=search))

        context = {
            'sdata': sdata,
            'category': category,
            'subcategory': subcategory,
            'randsubcat': randsubcat,
            'user': user,
            'userprofile': user_profile,
            'count_cart': count_cart,
        }
        return render(request, 'user/search.html', context)
    else:
        return HttpResponseRedirect('/')


def Cart_View(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        cart_items = Cart.objects.filter(user_id=user.id)

        total_cart_amount = 0

        for item in cart_items:
            item.total_amount = item.quantity * item.product.price
            total_cart_amount += item.total_amount

        count_cart = Cart.objects.filter(user_id=request.user).count()

        shipping_charge = 0
        if total_cart_amount  >= 100000:
            shipping_charge += 0
        elif total_cart_amount >= 20000:
            shipping_charge += 40
        elif total_cart_amount >= 10000:
            shipping_charge += 70
        else:
            shipping_charge += 120

        total_amount_pay = shipping_charge + total_cart_amount

        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'cart_items':cart_items,
            'total_cart_amount':total_cart_amount,
            'count_cart':count_cart,
            'shipping_charge':shipping_charge,
            'total_amount_pay':total_amount_pay,
        }
        return render(request,'user/cart.html',context)
    else:
        return HttpResponseRedirect('/')


def Add_Cart(request,pk):
    if request.user.is_authenticated:

        user = User.objects.get(id=request.user.id)
        product = get_object_or_404(Product, id=pk)



        if Cart.objects.filter(user=user, product=product).exists():
            messages.warning(request, "This product is already in your cart.")
        else:
            wish_item = Wishlist.objects.filter(user=user, product=product).first()
            if wish_item:
                wish_item.delete()  
            
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)

            messages.success(request, "Product added to your cart.")


        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def Remove_Cart(request,pk):
    if request.user.is_authenticated:   
        user = User.objects.get(id=request.user.id)
        cart_item = get_object_or_404(Cart, id=pk, user=user)
        cart_item.delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')

def Update_Cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            action = request.POST.get('action')
            cart_item_id = request.POST.get('cart_item_id')

            if action == 'minus':
                cart_item = Cart.objects.get(pk=cart_item_id)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()

            elif action == 'plus':
                cart_item = Cart.objects.get(pk=cart_item_id)
                cart_item.quantity += 1
                cart_item.save()

        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')


def Wishlist_View(request):  
    if request.user.is_authenticated:
        category, subcategory, randsubcat  = usernav_view(request)
        
        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        wish_items = Wishlist.objects.filter(user_id=user.id)

        count_cart = Cart.objects.filter(user_id=request.user).count()
        count_wishlist = Wishlist.objects.filter(user_id=request.user).count()
        
        context = {
            'category':category,
            'subcategory':subcategory,
            'randsubcat':randsubcat,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
            'wish_items':wish_items,
            'count_wishlist':count_wishlist,
        }
        return render(request,'user/wishlist.html',context)
    else:
        return HttpResponseRedirect('/')

def Add_Wishlist(request,pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        product = get_object_or_404(Product, id=pk)
        
        if Wishlist.objects.filter(user=user, product=product).exists():
            messages.warning(request, "This product is already in your wishlist.")
        else:
            wish_item, created = Wishlist.objects.get_or_create(user=user, product=product)
            messages.success(request, "Product added to your wishlist.")
        
        return HttpResponseRedirect('/userindex/')
    else:
        return HttpResponseRedirect('/')

def Remove_Wishlist(request,pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        wish_item = get_object_or_404(Wishlist, id=pk, user=user)
        wish_item.delete()
        return HttpResponseRedirect('/wishlist/')
    else:
        return HttpResponseRedirect('/')


def Profile(request):
    if request.user.is_authenticated:
        category, subcategory, randsubcat = usernav_view(request)

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)
        
        if request.method == 'POST':
            profileForm = CustomerProfileForm(request.POST, request.FILES, instance=user_profile)
            userForm = CustomerUserForm(request.POST, instance=user)
            
            if userForm.is_valid() and profileForm.is_valid():
                userForm.save()
                profileForm.save()
                messages.success(request, 'Profile updated successfully')
                return HttpResponseRedirect('/profile/')

            old_password = request.POST.get('oldpassword')
            new_password = request.POST.get('newpassword')
            renewpassword = request.POST.get('renewpassword')

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/profile/')
            else:
                messages.success(request, 'Invalid old password')
                return HttpResponseRedirect('/profile/')

        else:
            userForm = CustomerUserForm(instance=user)
            profileForm = CustomerProfileForm(instance=user_profile)

        
        count_cart = Cart.objects.filter(user_id=request.user).count()

        context = {
            'category': category,
            'subcategory': subcategory,
            'randsubcat': randsubcat,
            'profileForm': profileForm,
            'userForm': userForm,
            'user':user,
            'userprofile':user_profile,
            'count_cart':count_cart,
        }
        return render(request, 'user/profile.html', context)
    else:
        return HttpResponseRedirect('/')


def Signup_view(request):
    if request.user.is_superuser and request.user.is_authenticated:
        return HttpResponseRedirect('/admin-dashboard/')
    elif request.user.is_authenticated:
        return HttpResponseRedirect('/userindex/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            recaptcha_response = request.POST.get('g-recaptcha-response')

            if User.objects.filter(username=username).exists():
                context = {'error': 'Username is already taken.'}
                return render(request, 'user/signup.html', context)
            elif User.objects.filter(email=email).exists():
                context = {'error': 'Email is already registered.'}
                return render(request, 'user/signup.html', context)

            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }

            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            
            if result['success']:
                User.objects.create_user(username=username, email=email, password=password)
                return HttpResponseRedirect('/login/')
            else:
                context = {'error': 'Invalid reCAPTCHA. Please try again.'}
                return render(request, 'user/signup.html', context)

        context = {}
        return render(request,'user/signup.html',context)

def Login_view(request):
    if request.user.is_superuser and request.user.is_authenticated:
        return HttpResponseRedirect('/admin-dashboard/')
    elif request.user.is_authenticated:
        return HttpResponseRedirect('/userindex/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me', False)

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                
                if user.is_superuser:
                    if not remember_me:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(7 * 24 * 60 * 60)

                    messages.success(request, 'Login successfully')
                    return HttpResponseRedirect('/admin-dashboard/')
                else:
                    if not remember_me:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(7 * 24 * 60 * 60)

                    messages.success(request, 'Login successfully')
                    return HttpResponseRedirect('/userindex/')
            else:
                messages.warning(request, 'Invalid username or password')
        context = {}
        return render(request,'user/login.html',context)

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


UserModel = get_user_model()

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserModel.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "user/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': request.get_host(),
                        'site_name': 'multishop',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset_done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="user/password_reset.html", context={"password_reset_form":password_reset_form})

def password_reset_confirm(request, uidb64=None, token=None):
    if uidb64 is not None and token is not None:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('/reset_password_complete/')
            else:
                form = SetPasswordForm(user)
            return render(request, 'user/password_reset_confirm.html', {'form': form})
        else:
            return render(request, 'user/password_reset_invalid.html')
    return redirect('/')

def password_reset_complete(request):
    return render(request, 'user/password_reset_complete.html')

def password_reset_done(request):
    return render(request, 'user/password_reset_done.html')


def adminbase_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        context = {
            'user':user,
            'userprofile':user_profile,
        }

        return render(request,'admin/adminbase.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def adminprofile_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        
        if request.method == 'POST':
            profileForm = CustomerProfileForm(request.POST, request.FILES, instance=user_profile)
            userForm = CustomerUserForm(request.POST, instance=user)
            
            if userForm.is_valid() and profileForm.is_valid():
                userForm.save()
                profileForm.save()
                messages.success(request, 'Profile updated successfully')
                return HttpResponseRedirect('/admin-profile/')

            old_password = request.POST.get('oldpassword')
            new_password = request.POST.get('newpassword')
            renewpassword = request.POST.get('renewpassword')

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/admin-profile/')
            else:
                messages.success(request, 'Invalid old password')
                return HttpResponseRedirect('/admin-profile/')

        else:
            userForm = CustomerUserForm(instance=user)
            profileForm = CustomerProfileForm(instance=user_profile)


        context = {
            'profileForm': profileForm,
            'userForm': userForm,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/admin_profile.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def admin_add_maincategory_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)
        

        catname = request.POST.get('catname')
        catexist = Category.objects.filter(catname=catname)
        if catexist.exists():
            messages.success(request, 'Category already exists')
            return HttpResponseRedirect('/admin-add-maincategory/')
        if request.method == 'POST':
            categoryForm = category_form(request.POST)
            if categoryForm.is_valid():
                categoryForm.save()
                categoryForm = category_form()
                messages.success(request, 'Category added successfully.')
        else:
            categoryForm = category_form()
        cat = Category.objects.all().order_by('id')
        cus_cat_data=[]
        counter = 1
        for i in cat:
            cus_cat_data.append({'custom_id': counter, 'cat_data':i})
            counter += 1

        context = {
            'categoryForm': categoryForm,
            'cat': cus_cat_data,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/mainCategory.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def delete_maincategory_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        cat = Category.objects.get(id=pk)
        cat.delete()
        return HttpResponseRedirect('/admin-add-maincategory/')
    else:
        return HttpResponseRedirect('/userindex/')

def update_category_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        cat = Category.objects.get(id=pk)
        if request.method == 'POST':
            categoryForm = category_form(request.POST,instance=cat)
            if categoryForm.is_valid():
                categoryForm.save()
                messages.success(request, 'Category updated successfully.')
                return HttpResponseRedirect('/admin-add-maincategory/')
        else:
            categoryForm = category_form(instance=cat)
        cat = Category.objects.all().order_by('id')
        cus_cat_data=[]
        counter = 1
        for i in cat:
            cus_cat_data.append({'custom_id': counter, 'cat_data':i})
            counter += 1

        context = {
            'categoryForm': categoryForm,
            'cat': cus_cat_data,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/update_mainCategory.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def admin_subcategory_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        subcat = Subcategory.objects.select_related('category').all().order_by('id')
        cus_subcat_data=[]
        counter = 1
        for i in subcat:
            cus_subcat_data.append({'custom_id': counter, 'subcat_data':i})
            counter += 1
        context = {
            'subcat': cus_subcat_data,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/subCategory.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def admin_add_subcategory_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        if request.method == 'POST':
            subcategoryForm = subcategory_form(request.POST, request.FILES)
            if subcategoryForm.is_valid():
                subcategoryForm.save()
                subcategoryForm = subcategory_form()
                messages.success(request, 'Subcategory added successfully.')
                return HttpResponseRedirect('/admin-subcategory/')
        else:
            subcategoryForm = subcategory_form()

        context = {
            'subcategoryForm': subcategoryForm,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/add_subcategory.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def delete_subcategory_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        subcat = Subcategory.objects.get(id=pk)
        subcat.delete()
        return HttpResponseRedirect('/admin-subcategory/')
    else:
        return HttpResponseRedirect('/userindex/')

def update_subcategory_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        subcat = Subcategory.objects.get(id=pk)
        if request.method == 'POST':
            subcategoryForm = subcategory_form(request.POST, request.FILES, instance=subcat)
            if subcategoryForm.is_valid():
                subcategoryForm.save()
                messages.success(request, 'Subcategory updated successfully.')
                return HttpResponseRedirect('/admin-subcategory/')
        else:
            subcategoryForm = subcategory_form(instance=subcat)
        context = {
            'subcategoryForm': subcategoryForm,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/update_subcategory.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def admin_product_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        product = Product.objects.select_related('subcategory').all().order_by('id')
        cus_product_data=[]
        counter = 1
        for i in product:
            cus_product_data.append({'custom_id': counter, 'product_data':i})
            counter += 1

        context = {
            'product':cus_product_data,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/product.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

def admin_add_product_view(request):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        productForm  = product_form()
        imageForm  = productimage_form()

        if request.method == 'POST':
            productForm = product_form(request.POST, request.FILES)
            imageForm = productimage_form(request.POST, request.FILES)

            if productForm.is_valid():
                product = productForm.save()

                files = request.FILES.getlist('images')
                for file in files:
                    ProductImage.objects.create(product=product,images=file)

                messages.success(request, 'Product added successfully.')
                return HttpResponseRedirect('/admin-product/')
        else:
            productForm = product_form()
            imageForm  = productimage_form()

        context = {
            'productForm': productForm,
            'imageForm': imageForm,
            'user':user,
            'userprofile':user_profile,
        }

        return render(request,'admin/add_product.html',context)
    else:
        return HttpResponseRedirect('/userindex/')

    
def delete_product_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=pk)
        product.delete()

        messages.success(request, 'Product deleted successfully.')
        return HttpResponseRedirect('/admin-product/')
    else:
        return HttpResponseRedirect('/userindex/')

def update_product_view(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:

        user = User.objects.get(id=request.user.id)
        user_profile, created = CustomerProfile.objects.get_or_create(user_id=user.id)

        product = Product.objects.get(id=pk)
        product_images = ProductImage.objects.filter(product=product)

        if request.method == 'POST':
            files = request.FILES.getlist('images')
            productForm = product_form(request.POST, request.FILES, instance=product)
            imageForm = productimage_form(request.POST, request.FILES)

            if productForm.is_valid():
                product=productForm.save()

                product_images.delete()

                
                for file in files:
                    ProductImage.objects.create(product=product,images=file)

                messages.success(request, 'Product updated successfully.')
                return HttpResponseRedirect('/admin-product/')
        else:
            productForm = product_form(instance=product)
            imageForm  = productimage_form()

        context = {
            'productForm': productForm,
            'imageForm':imageForm,
            'product_images':product_images,
            'user':user,
            'userprofile':user_profile,
        }
        return render(request,'admin/update_product.html',context)
    else:
        return HttpResponseRedirect('/userindex/')
