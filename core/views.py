from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from Tavel import settings
from .forms import BookingForm, UserRegisterForm, UserLoginForm, FeedbackForm
from .models import *
import requests
from django.utils.translation import gettext_lazy as _
from .services import WeatherService


# @cache_page(60 * 15)
def home(request):
    places = Places.objects.all()[0:4]
    blogs = TourBlog.objects.all()
    paginator = Paginator(blogs, 1)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'core/index.html', {'places': places, 'blogs': blogs, 'page_obj': page_obj})


# @cache_page(60 * 15)
def cities_hotels(request):
    cities = Cities.objects.all()
    hotels = Hotels.objects.all()
    return render(request, 'core/cities_hotels.html',
                  {'cities': cities, 'hotels': hotels})


# @cache_page(60 * 15)
def tours(request):
    places = Places.objects.all()
    paginator = Paginator(places, 4)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'core/tours.html', {'places': places, 'page_obj': page_obj})


class Search(ListView):
    template_name = 'core/search.html'
    places = Places.objects.all()
    extra_context = {'places': places}
    paginate_by = 1

    def get_queryset(self):
        location = self.request.GET.get('Location')
        price1 = int(self.request.GET.get('Price1'))
        price2 = int(self.request.GET.get('Price2'))
        my_range = range(price1, price2)
        list_range = list(my_range)
        object_list = Places.objects.filter(Q(title__icontains=location) & Q(cost__in=list_range))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = self.request.GET.get('Location')
        context[
            'q'] = f"Location={self.request.GET.get('Location')}&Price1={int(self.request.GET.get('Price1'))}&Price2={int(self.request.GET.get('Price2'))}&"
        return context


# @cache_page(60 * 15)
def view_city(request, slug):
    city = Cities.objects.get(slug=slug)
    return render(request, 'core/view_city.html', {'city': city})


# @cache_page(60 * 15)
def view_hotels(request, slug):
    hotel = Hotels.objects.get(slug=slug)
    return render(request, 'core/view_hotels.html', {'hotel': hotel})


# @cache_page(60 * 15)
def view_blog(request, slug):
    blog = TourBlog.objects.get(slug=slug)
    blog.views = F('views') + 1
    blog.save()
    blog.refresh_from_db()
    return render(request, 'core/view_blog.html', {'blog': blog})


# @cache_page(60 * 15)
def view_tour(request, slug):
    tour = Places.objects.get(slug=slug)
    tour_people = tour.people
    # tour_bookings = tour.books.count()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                # Check if the user has already booked
                selected_date = form.cleaned_data['date']
                bookings_count = Booking.objects.filter(date=selected_date).count()
                user_bookings = Booking.objects.filter(user=request.user, date=selected_date)
                if user_bookings.exists() or tour_people <= bookings_count:
                    # Redirect or display a message indicating the user has already booked
                    messages.error(request, _("You have already booked or people count limited"))
                else:
                    # Save the booking
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.tour = tour
                    booking.save()
                    messages.success(request, _("You booked successfully!"))
        else:
            return redirect('sign-in')
    else:
        form = BookingForm()
    return render(request, 'core/view_tour.html', {'tour': tour, 'form': form})


# @cache_page(60 * 15)
def create_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Successfully sign up!"))
            return redirect('sign-up')
        else:
            messages.error(request, _("Sorry...but we find some issue, try again"))
    else:
        form = UserRegisterForm()
    return render(request, 'core/signup.html', {'form': form})


# @cache_page(60 * 15)
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _("Successfully sign in!"))
            return redirect('sign-in')
        else:
            messages.error(request, _("Sorry...but we find some issue, try again"))
    else:
        form = UserLoginForm()
    return render(request, 'core/signin.html', {'form': form})


# @cache_page(60 * 15)
def user_logout(request):
    logout(request)
    return redirect('sign-in')


# @cache_page(60 * 15)
def explore_more(request):
    more = Explore_More.objects.all()
    return render(request, 'core/explore_more.html', {'more': more})


# @cache_page(60 * 15)
def view_more(request, slug):
    more = Explore_More.objects.get(slug=slug)
    return render(request, 'core/view_more.html', {'more': more})


# @cache_page(60 * 15)
def privacy(request):
    return render(request, 'core/privacy.html')


def about(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            subject = form.cleaned_data['subject']
            message = f'Email: {feedback.email}\nMessage: {feedback.subject}'
            from_email = form.cleaned_data['email']  # Replace with your email address
            to_email = settings.DEFAULT_FROM_EMAIL
            mail = send_mail(subject, message, from_email, [to_email], fail_silently=True)
            if mail:
                form.save()
                messages.success(request, _('Message successfully send'))
            else:
                feedback.delete()
                messages.error(request, _('Internet connection has lost'))
        else:
            messages.error(request, _('Validation failure'))
            return redirect('about')
    else:
        form = FeedbackForm()

    return render(request, 'core/about.html', {'form': form})


# @cache_page(60 * 15)
def get_weather(request, city):
    places = Places.objects.all()
    blogs = TourBlog.objects.all()
    paginator = Paginator(blogs, 1)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = f'http://api.openweathermap.org/data/2.5/weather/'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return render(request, 'core/weather.html', {'weather_data': data, 'places': places, 'blogs': blogs, 'page_obj': page_obj})


# @cache_page(60 * 15)
def weekly_weather_forecast(request, city):
    api_key = settings.OPENWEATHERMAP_API_KEY
    weather_service = WeatherService(api_key)
    forecast_data = weather_service.get_weekly_forecast(city)

    return render(request, 'core/weekly_forecast.html', {'forecast_data': forecast_data})


def weekly_forecast(request):
    return render(request, 'core/forecast_list.html')

