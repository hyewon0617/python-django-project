import json
import math

import requests
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.conf import settings

from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from meokjeul.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from meokjeul.models import Restaurant, Review


# Create your views here.
def list(request):
    restaurants = Restaurant.objects.all().order_by('-created_at').annotate(reviews_count=Count('review')) \
        .annotate(average_point=Avg('review__point'))  # __ + 속성명
    paginator = Paginator(restaurants, 5)
    page = request.GET.get('page')
    if page is None:
        page = 1

    # 시작페이지 끝페이지 구하기
    page_F = float(page)
    if page_F <= 10:
        beginPage = 1
    else:
        beginPage = (math.trunc(page_F / 10)) * 10 + 1

    if (beginPage + 10) > paginator.num_pages:
        lastPage = paginator.num_pages
    else:
        lastPage = beginPage + 9
    nextRangeStartPage = lastPage + 1

    pageRange = []
    for num in range(beginPage, lastPage + 1):
        pageRange.append(num)

    items = paginator.get_page(page)
    context = {
        'restaurants': items,
        'lastPage': lastPage,
        'pageRange': pageRange,
        'nextRangeStartPage': nextRangeStartPage,
    }
    return render(request, 'meokjeul/list.html', context)


def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/')
    form = RestaurantForm()
    return render(request, 'meokjeul/create.html', {'form': form})


def update_passwordCheck(request):
    if request.method == 'POST' and 'id' in request.POST:
        item = get_object_or_404(Restaurant, pk=request.POST.get('id'))
        password = request.POST.get('password', '')
        if password == item.password:
            return HttpResponse("match")
        else:
            return HttpResponse("not match")


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        # item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk=request.POST.get('id'))
        # password = request.POST.get('password', '')
        form = UpdateRestaurantForm(request.POST, instance=item)

        if form.is_valid(): # and password == item.password
            item = form.save()
    elif request.method == 'GET':
        # item = Restaurant.objects.get(pk=request.GET.get('id')) ## meokjeul/update?id=2
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'meokjeul/update.html', {'form': form})
    return HttpResponseRedirect('/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('/')
        else:
            messages.info(request, "암호가 일치하지 않습니다.")
    return render(request, 'meokjeul/delete.html', {'item': item})


def detail(request, id):
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'meokjeul/detail.html', {'item': item, 'reviews': reviews})
    return HttpResponseRedirect('/')


def search(request):
    items = Restaurant.objects.all().order_by('-created_at').annotate(reviews_count=Count('review')) \
        .annotate(average_point=Avg('review__point'))

    q = request.POST.get('q', "")

    if q:
        items = items.filter(name__icontains=q)
        return render(request, 'meokjeul/search.html', {'items': items, 'q': q})
    else:
        return render(request, 'meokjeul/search.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['pwd']
        user = auth.authenticate(request, username=email, password=pwd)
        if user is None:
            messages.info(request, "존재하지 않는 아이디, 비밀번호입니다.")
        else:
            auth.login(request, user)
            return redirect('/')
    return render(request, 'meokjeul/login.html')


def join(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['pwd']
        if not (email and pwd):
            messages.info(request, "이메일과 비밀번호를 입력해야 합니다.")
        elif User.objects.filter(username=email).exists():
            messages.info(request, "이미 존재하는 아이디입니다.")
        else:
            User.objects.create_user(username=email, password=pwd)
            return redirect('/')
    return render(request, 'meokjeul/join.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page = request.GET.get('page')
    if page is None:
        page = 1

    # 시작페이지 끝페이지 구하기
    page_F = float(page)
    if page_F <= 10:
        beginPage = 1
    else:
        beginPage = (math.trunc(page_F / 10)) * 10 + 1

    if (beginPage + 10) > paginator.num_pages:
        lastPage = paginator.num_pages
    else:
        lastPage = beginPage + 9
    nextRangeStartPage = lastPage + 1

    pageRange = []
    for num in range(beginPage, lastPage + 1):
        pageRange.append(num)

    items = paginator.get_page(page)
    context = {
        'reviews': items,
        'lastPage': lastPage,
        'pageRange': pageRange,
        'nextRangeStartPage': nextRangeStartPage,
    }

    return render(request, 'meokjeul/review_list.html', context)


def review_create(request, restaurant_id):
    form = ReviewForm(request.POST)
    if request.method == 'POST':
        # print(request.POST)

        if form.is_valid():
            user_id = request.session['_auth_user_id']

            new_item = form.save(commit=False)
            new_item.author_id = user_id
            new_item.save()
        return redirect('restaurant-detail', id=restaurant_id)
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item})
    return render(request, 'meokjeul/review_create.html', {'form': form, 'item': item})


def review_update(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)

    if request.user != item.author:
        messages.info(request, '수정할 수 있는 권한이 없습니다.')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('restaurant-detail', id=restaurant_id)
    else:
        form = ReviewForm(instance=item)
    return render(request, 'meokjeul/review_update.html', {'form': form})


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)

    if request.user != item.author and not request.user.is_staff:
        messages.info(request, '삭제할 수 있는 권한이 없습니다.')

    if request.method == 'POST':
        item.delete()
        return redirect('restaurant-detail', id=restaurant_id)
    else:
        return render(request, 'meokjeul/review_delete.html', {'item': item})


def findAddress(request):
    return render(request, 'meokjeul/findAddress.html')


def findAddressProc(request):
    if request.method == 'POST':
        address = request.POST.get("address", None)
        URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?"
        URL += "query=" + address

        headers = {
            'X-NCP-APIGW-API-KEY-ID': "8jxb8lmspl",
            'X-NCP-APIGW-API-KEY': getattr(settings, 'API_KEY', 'API_KEY')
        }

        response = requests.get(URL, headers=headers)
        if response.status_code == 200:

            result = json.loads(response.text)

            cnt = result.get("meta").get("totalCount")  # 결과 개수
            if (cnt == 0):
                code = 0
                coord = {"resultCode": code}
            else:
                addressobj = result.get("addresses")[0]  # 'addresses' 의 0번째 배열 가져오기
                x = addressobj.get("x")
                y = addressobj.get("y")
                road = addressobj.get("roadAddress")
                jibun = addressobj.get("jibunAddress")
                code = 1
                coord = {"resultCode": code, "x": x, "y": y, "road": road, "jibun": jibun}

        else:
            print(response.status_code)
            print(response.text)

    return HttpResponse(json.dumps(coord))
