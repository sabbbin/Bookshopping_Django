from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import book, orderbook,order,history
#from django import get_object_or_404, get_or_create



#from .models import profile
User=get_user_model()
# Create your views here.
from .forms import UserCreationForm, userloginform, UserChangeForm
def register(request,*args,**kwargs):
    
    form=UserCreationForm(request.POST or None)
    if form.is_valid():
        print('usercreated')
        form.save()
        return HttpResponseRedirect("/login")
        
    return render(request, "account/register.html", {"form":form})    
@login_required()
def change(request ,*args, **kwargs):
    print(request.user)
    ins=User.objects.get(email=request.user)
    form =UserChangeForm(request.POST or None, instance=ins)
    print('changed')
    if form.is_valid():
        print('changed')
        form.save()
        return render(request,'account/login.html')
        
    return render(request, "account/change.html", {"form":form})   


def loginn(request,*args,**kwargs):
    form=userloginform(request.POST or None)
    if form.is_valid():
        usernam=form.cleaned_data.get('username')
        print(usernam)
        user_=User.objects.get(username__iexact=usernam)
        
        
        login(request, user_)
        return redirect("list_book")
        
        print('success')
    return render(request, "account/login.html", {"form":form})    


class detailview(DetailView):
    model=book


class listview(ListView):
    model=book


class cartlist(DetailView):
    model=order

@login_required()
def add_to_cart(request,slug):
    Book=get_object_or_404(book,slug=slug)
    
    order_book,created=orderbook.objects.get_or_create(book=Book)
    print(request.user)
    order_book.Price=Book.price

    order_qs=order.objects.filter(user=request.user)
    
    if order_qs.exists():
        print('b')
        Order=order_qs[0]
        if Order.books.filter(book__slug=Book.slug).exists():
            
            order_book.quantity+=1
            order_book.totalprice+=Book.price
           
            Order.sum+=Book.price
            Order.save()
            order_book.save()
        else:
            Order.books.add(order_book)
            Order.save()
            Order.slug=Order.slugg()  
            Order.sum+=Book.price
            
            order_book.Price=Book.price
            order_book.quantity=1
            order_book.totalprice=Book.price
            order_book.save()
            Order.save()
    else:
        print('a')
        
        Order,created=order.objects.get_or_create(user=request.user,
                                                    books__book=Book )
        a=request.user
        Order.slug=Order.slugg()  
        Order.sum+=Book.price
        order_book.Price=Book.price
        order_book.quantity=1
        order_book.totalprice=Book.price
        print('haha')
        print(order_book)
        Order.books.add(order_book)
        Order.save()
        order_book.save()
       
    print('successful')    
    
    return redirect("cart_list",slug=Order)
    #return  HttpResponseRedirect("/cartlist/{num}",num=slug)
    




@login_required()
def remove_to_cart(request,slug):
   
    order_qs=order.objects.filter(user=request.user)
    print(order_qs[0])
    Book=orderbook.objects.filter(book__title=slug).first()
    print(Book)
    

    
    BooK=get_object_or_404(order_qs,books=Book)
    Order=order_qs[0]
    if BooK.books.exists():
      
        if (Book.quantity>0):
            Book.quantity-=1
            Book.totalprice-=Book.Price
            Order.sum-=Book.Price
            Order.save()
            Book.save()
            
    return redirect("cart_list", slug=order_qs[0])


@login_required()
def history_display(request):
  
    ins=history.objects.filter(user=request.user)
  
    return render(request, "account/viewhistory.html", {"object":ins})   

@login_required()
def history_insert(request):
    
    order_qs=order.objects.filter(user=request.user)
   


    a=orderbook.objects.all()
    count=orderbook.objects.count()
    
    for i in range (0,count):
        h=history()
        
        h.user=request.user
        h.book=a[i].book
        print (h.book)
        h.quantity=a[i].quantity
        h.Price=a[i].Price
        h.totalprice=a[i].totalprice
        
        #sBook=book.objects.filter(book__title=orderbook.book).first()

    
        h.image=a[i].book.image
        h.save() 

      
    emp = orderbook.objects.all()
    emp1 = order.objects.all()
    emp.delete()    
    emp1.delete()
    return redirect("login")



    
    



@login_required
def logout(request):
    django_logout(request)
    
    return redirect("login")





def delete(request):
   emp = orderbook.objects.all()
   emp1 = order.objects.all()
   emp.delete()    
   emp1.delete()
   return redirect("login")