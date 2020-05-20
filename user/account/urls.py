from django.urls import  path
from .views import (loginn,register,
                    change,detailview,listview,
                    add_to_cart,
                    cartlist,
                    remove_to_cart,
                    login_required,
                    logout,
                    delete,
                    history_insert,
                    history_display)
urlpatterns=[

    path('register/',register, name='register'),
    
    path('login/', loginn, name='login'),
    path('change/',change, name='change'),
    path('detail/<slug:slug>/',detailview.as_view(), name='book_detail'),
    path('list/',listview.as_view(), name='list_book'),
    path('addtocart/<slug:slug>/',add_to_cart, name='addtocart'),
    path('cartlist/<slug:slug>/',cartlist.as_view(), name='cart_list'),
    path('removetocart/<slug:slug>/',remove_to_cart, name='removetocart'),
    path('logout/',logout, name='logout'),
    path('delete/',delete, name='delete'),
    path('history/', history_insert, name='historyinsert'),
    path('historys/', history_display, name='historyview'),

]