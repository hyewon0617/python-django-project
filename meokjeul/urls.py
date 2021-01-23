from django.urls import path

from . import views
urlpatterns =[
    path('', views.list, name="list"),
    path('create/', views.create, name="restaurant-create"),
    path('update/', views.update, name="restaurant-update"),
    path('update/checkPw', views.update_passwordCheck, name="restaurant-update-pwcheck"),
    # path('detail/', views.detail, name="restaurant-detail"),
    path('restaurant/<int:id>/delete', views.delete, name="restaurant-delete"),
    path('restaurant/<int:id>/', views.detail, name="restaurant-detail"),
    path('search/', views.search, name="search"),

    path('login/', views.login, name="login"),
    path('join/', views.join, name="join"),
    path('logout/', views.logout, name="logout"),

    path('review/list/', views.review_list, name="review-list"),
    path('restaurant/<int:restaurant_id>/review/create/', views.review_create, name="review-create"),
    path('restaurant/<int:restaurant_id>/review/delete/<int:review_id>', views.review_delete, name="review-delete"),
    path('restaurant/<int:restaurant_id>/review/update/<int:review_id>', views.review_update, name="review-update"),

    path('create/findAddress/', views.findAddress, name="findAddress"),
    path('create/findAddressProc/', views.findAddressProc, name="findAddressProc"),
    path('update/findAddress/', views.findAddress, name="findAddress"),
    path('update/findAddressProc/', views.findAddressProc, name="findAddressProc"),
]

