from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

Velayats = (
    ('Mary', 'Mary'),
    ('Ahal', 'Ahal'),
    ('Lebap', 'Lebap'),
    ('Balkan', 'Balkan'),
    ('Daşoguz', 'Daşoguz'),
    ('Aşgabat', 'Aşgabat')
)

During_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
)


class TourPlan(models.Model):
    days_during = models.IntegerField(choices=During_CHOICES, verbose_name='Длительность')
    content1 = models.TextField(blank=True, verbose_name='День 1')
    content2 = models.TextField(blank=True, verbose_name='День 2')
    content3 = models.TextField(blank=True, verbose_name='День 3')
    content4 = models.TextField(blank=True, verbose_name='День 4')
    content5 = models.TextField(blank=True, verbose_name='День 5')
    content6 = models.TextField(blank=True, verbose_name='День 6')
    content7 = models.TextField(blank=True, verbose_name='День 7')

    def __str__(self):
        return str(self.days_during)

    class Meta:
        verbose_name = 'План тура'
        verbose_name_plural = 'Планы тура'


class Places(models.Model):
    # tour_days = models.IntegerField(default=0)
    title = models.CharField(max_length=255, verbose_name='Названия тура')
    tour_plan = models.ForeignKey(TourPlan, models.PROTECT, verbose_name='План тура')
    people = models.IntegerField(default=0, verbose_name='Кол-во людей')
    group = models.IntegerField(default=0, verbose_name='Кол-во групп')
    inf_content = models.TextField(verbose_name='Инфо про тур')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    cost = models.IntegerField(default=0, verbose_name='Цена')
    slug = models.SlugField(verbose_name='url', help_text='Автозаполнение! Не трогать!')

    def get_absolute_url(self):
        return reverse('view_tour', kwargs={'slug': self.slug})

    # def __str__(self):
    #     return self.title

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class TourBlog(models.Model):
    title = models.CharField(max_length=255,verbose_name='Названия блога')
    content = models.TextField(verbose_name='Контент блога')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', help_text='Автозаполнение! Не трогать!')
    views = models.IntegerField(default=0, verbose_name='Просмотры', help_text='Автозаполнение! Не трогать!')
    slug = models.SlugField(verbose_name='url', help_text='Автозаполнение! Не трогать!')

    def get_absolute_url(self):
        return reverse('view_blog', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-created_at']

class Cities(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название города')
    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Главная фото')
    velayat = models.CharField(choices=Velayats, max_length=45, verbose_name='Велаят')
    info = models.TextField(verbose_name='Инфо про город')
    img1 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img2 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img3 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img4 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img5 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img6 = models.ImageField(upload_to='cities/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    slug = models.SlugField(verbose_name='url', help_text='Автозаполнение! Не трогать!')

    def get_absolute_url(self):
        return reverse('view_city', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Hotels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название отелья')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT,verbose_name='Город')
    info = models.TextField(verbose_name='Инфо про отель')
    cost = models.IntegerField(default=0, verbose_name='Цена')
    build_in = models.DateField(verbose_name='Построина в')
    stars = models.IntegerField(default=0, verbose_name='Звезды')
    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Главная фото')
    img1 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img2 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img3 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img4 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img5 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    img6 = models.ImageField(upload_to='hotels/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    slug = models.SlugField(verbose_name='url', help_text='Автозаполнение! Не трогать!')

    def get_absolute_url(self):
        return reverse('view_hotels', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ползователь')
    tour = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='books', verbose_name='Брон')
    date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return f'{self.user.username} - {self.tour}'

    class Meta:
        verbose_name = 'Брон'
        verbose_name_plural = 'Броны'


class Explore_More(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Инфо')
    slug = models.SlugField(unique=True, verbose_name='url', help_text='Автозаполнение! Не трогать!')

    def get_absolute_url(self):
        return reverse('view_more', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Explore more'
        verbose_name_plural = 'Explore more'


class Feedback(models.Model):
    user = models.CharField(max_length=255, verbose_name='Ползователь')
    email = models.EmailField(null=True)
    subject = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

