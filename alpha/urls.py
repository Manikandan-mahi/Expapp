from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.v_index, name='Index'),
    path('login/', views.v_login,name='Login'),
    path('register/',views.v_register,name='Register'),
    path('add/<str:expense>/<int:amount>/<str:desc>/<str:expdate>', views.v_add, name='AddExp'),
    path('add_inc/<str:inc>/<int:amount>/<str:desc>/<str:incdate>', views.v_add_inc, name='AddInc'),
    path('update/<int:eid>/<str:expense>/<int:amount>/<str:desc>/<str:expdate>', views.v_update, name='UpdateExp'),
    path('update_inc/<int:iid>/<str:inc>/<int:amount>/<str:desc>/<str:incdate>', views.v_update_inc, name='UpdateInc'),
    path('delete/<int:expid>/<str:expdate>', views.v_delete, name='DeleteExp'),
    path('delete_inc/<int:incid>/<str:incdate>', views.v_delete_inc, name='DeleteInc'),
    path('home/<str:sdate>',views.v_home,name='Home'),
    path('profile/', views.v_profile, name="Profile"),
    path('report/<str:mon>/<str:yr>',views.v_report,name="Report"),
    path('find/<str:p_txn_name>' , views.v_find , name = "FindTxn" ),
    path('find/' , views.v_find , name = "Find" ),
    path('logout/',views.v_logout, name="Logout"),
    
]