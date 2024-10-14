from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
import requests

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin

from project import settings
from .forms import PaymentForm1, PaymentForm2, SongRequestForm, ServiceAdClipRequestForm, ServiceAdMusicRequestForm
from .models import Category, Tag, ServiceCongratsByTag, Name, ServiceCongratsByName, PoemByName, Blog, Review, \
    Subcategory, ServiceSongs, ServiceSongsVideo, ServiceVideoAdvertisement, ServiceAdvertisement, ServiceAdClipPrice
from .services import get_grouped_names


class ServiceCongratsByTagListView(ListView):
    """
    Отображает список поздравлений по тегу
    """
    model = ServiceCongratsByTag
    template_name = 'musprivet/congrat_list.html'
    context_object_name = 'congrats'

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = ServiceCongratsByTag.objects.all()
            tag_slug = self.kwargs.get('tag_slug', None)
            name_slug = self.kwargs.get('name_slug', None)
            if tag_slug and not name_slug:
                try:
                    tag = getattr(Tag.objects.get(slug=tag_slug), 'id')
                    queryset = queryset.filter(tag=tag)
                except Tag.DoesNotExist:
                    return HttpResponseNotFound()
            else:
                queryset = queryset.none()

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'mus-pozdrav'
        category = get_object_or_404(Category, slug=category_url)
        tag_slug = self.kwargs.get('tag_slug', None)
        name_slug = self.kwargs.get('name_slug', None)
        if tag_slug and not name_slug:
            try:
                context['grouped_names'] = get_grouped_names(tag_slug)
                current_tag = get_object_or_404(Tag, slug=tag_slug)
                context['current_tag'] = current_tag
            except Tag.DoesNotExist:
                return get_object_or_404(Tag, slug=tag_slug)
        else:
            context['grouped_names'] = get_grouped_names('pozdravlenie-zhene-po-imeni')
            current_tag = Tag.objects.get(slug='pozdravlenie-zhene-po-imeni')
            context['current_tag'] = current_tag

        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['tags'] = Tag.objects.filter(category=category)
        context['articles'] = Blog.objects.all()
        context['reviews'] = Review.objects.filter(category=category)
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['description'] = 'Выберите готовое музыкальное поздравление в подарок любимым. ' + \
                                 category.name + ' ' + current_tag.name + ' Пришлем понравившийся ' \
                                                                          'аудио привет в формате мр3 на Вашу ' \
                                                                          'электронную почту. Поздравите лично ' \
                                                                          'со 100% гарантией!'
        context['url'] = self.request.build_absolute_uri((reverse('musprivet:congrat_list',
                                                            kwargs={'tag_slug': self.kwargs.get('tag_slug')})))
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)
        return context


class ServiceCongratsByTagDetailView(DetailView, FormMixin):
    """
    Отображает детальную страницу поздравления по тегу
    """
    model = ServiceCongratsByTag
    context_object_name = 'congrat'
    slug_field = 'congrat_slug'
    template_name = 'musprivet/congrat_detail.html'
    form_class = PaymentForm1

    def get_object(self, *args, **kwargs):
        return ServiceCongratsByTag.objects.get(slug=self.kwargs.get('congrat_slug'))

    def get_success_url(self):
        return reverse('musprivet:congrat_detail', kwargs={'tag_slug': self.kwargs.get('tag_slug'), 'congrat_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'mus-pozdrav'
        category = get_object_or_404(Category, slug=category_url)
        tag_slug = self.kwargs.get('tag_slug', None)
        current_tag = get_object_or_404(Tag, slug=tag_slug)
        context['current_tag'] = current_tag
        context['categories'] = Category.objects.all()
        context['form'] = self.get_form()
        context['price'] = ServiceAdClipPrice.objects.get(type='C')
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['description'] = 'Выберите готовое музыкальное поздравление в подарок любимым. ' + \
                                 category.name + ' ' + current_tag.name + ' ' + self.object.title + ' Пришлем понравившийся ' \
                                                                          'аудио привет в формате мр3 на Вашу ' \
                                                                          'электронную почту. Поздравите лично ' \
                                                                          'со 100% гарантией!'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:congrat_detail',
                                                                 kwargs={'tag_slug': self.kwargs.get('tag_slug'),
                                                                         'congrat_slug': self.object.slug}))
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        amount = int(ServiceAdClipPrice.objects.get(type='C').price) *100
        order_id = f'ORDER-{self.get_object().id}'
        description = form.cleaned_data['congratulation']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        key = settings.terminal_key

        payment_data = {
            'TerminalKey': key,
            'Amount': amount,
            'OrderId': order_id,
            'Description': description,
            'Email': email,
            'Phone': phone,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post('https://securepay.tinkoff.ru/v2/Init', json=payment_data, headers=headers)
        try:
            response_data = response.json()
        except JSONDecodeError:
            return HttpResponseNotFound()
        if response.status_code == 200 and 'PaymentURL' in response_data:
            payment_url = response_data['PaymentURL']
            form.instance.service = self.object
            form.instance.price = int(getattr(ServiceAdClipPrice.objects.get(type='C'), 'price'))
            form.save()
            return redirect(payment_url)


class PoemByNameDetailView(DetailView, FormMixin):
    """
    Отображает детальную страницу стихотворения по имени
    """
    model = PoemByName
    context_object_name = 'name_poem'
    template_name = 'musprivet/name_poem_detail.html'
    form_class = PaymentForm2

    def get_object(self, *args, **kwargs):
        tag_slug = self.kwargs.get('tag_slug', None)
        name_slug = self.kwargs.get('name_slug', None)
        if tag_slug and name_slug:
            tag = getattr(Tag.objects.get(slug=tag_slug), 'id')
            name = getattr(Name.objects.get(slug=name_slug), 'id')
            try:
                poem = PoemByName.objects.get(tag=tag, name=name)
                return poem
            except ObjectDoesNotExist:
                return PoemByName.objects.none()

    def get_success_url(self):
        return reverse('musprivet:name_poem_detail', kwargs={'tag_slug': self.kwargs.get('tag_slug'), 'name_slug': self.kwargs.get('name_slug')})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'mus-pozdrav'
        category = get_object_or_404(Category, slug=category_url)
        tag_slug = self.kwargs.get('tag_slug', None)
        current_tag = get_object_or_404(Tag, slug=tag_slug)
        if self.get_object():
            name_congrats = ServiceCongratsByName.objects.filter(poem=self.get_object())
            context['name_congrats'] = name_congrats
        context['current_tag'] = current_tag
        context['categories'] = Category.objects.all()
        context['price'] = ServiceAdClipPrice.objects.get(type='C')
        context['form'] = self.get_form()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        if self.object:
            context['description'] = 'Выберите готовое музыкальное поздравление в подарок любимым. ' + \
                                 category.name + ' ' + current_tag.name + ' ' + self.object.title + ' Пришлем понравившийся ' \
                                                                          'аудио привет в формате мр3 на Вашу ' \
                                                                          'электронную почту. Поздравите лично ' \
                                                                          'со 100% гарантией!'
        else:
            context['description'] = 'Выберите готовое музыкальное поздравление в подарок любимым. ' + \
                                 category.name + ' ' + current_tag.name + ' Пришлем понравившийся ' \
                                                                          'аудио привет в формате мр3 на Вашу ' \
                                                                          'электронную почту. Поздравите лично ' \
                                                                          'со 100% гарантией!'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:name_poem_detail',
                                                                 kwargs={'tag_slug': self.kwargs.get('tag_slug'),
                                                                         'name_slug': self.kwargs.get('name_slug')}))
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        amount = int(ServiceAdClipPrice.objects.get(type='C').price) *100
        order_id = f'ORDER-{form.cleaned_data["service"]}'
        description = form.cleaned_data['congratulation']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        key = settings.terminal_key

        payment_data = {
            'TerminalKey': key,
            'Amount': amount,
            'OrderId': order_id,
            'Description': description,
            'Email': email,
            'Phone': phone,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post('https://securepay.tinkoff.ru/v2/Init', json=payment_data, headers=headers)
        try:
            response_data = response.json()
        except JSONDecodeError:
            return HttpResponseNotFound()
        if response.status_code == 200 and 'PaymentURL' in response_data:
            payment_url = response_data['PaymentURL']
            form.instance.price = int(getattr(ServiceAdClipPrice.objects.get(type='C'), 'price'))
            form.save()
            return redirect(payment_url)


class ServiceSongsListView(ListView, FormMixin):
    """
    Отображает список песен на заказ
    """
    model = ServiceSongs
    template_name = 'musprivet/song_list.html'
    context_object_name = 'songs'
    form_class = SongRequestForm

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = ServiceSongs.objects.all()
            return queryset

    def get_success_url(self):
        return reverse('musprivet:song_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'podarit-pesnu'
        category = get_object_or_404(Category, slug=category_url)
        context['video_songs'] = ServiceSongsVideo.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = self.get_form()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['description'] = 'Песня в подарок любимой девушке, парню, родителям, мужу, жене. ' + \
                                 category.name + ' 100% шлягеры!'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:song_list'))
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class ServiceAdvertisementListView(ListView, FormMixin):
    """
    Отображает список услуг аудиорекламы
    """
    model = ServiceAdvertisement
    template_name = 'musprivet/ads_list.html'
    context_object_name = 'ads'

    def get_form_class(self):
        subcategory_slug = self.kwargs.get('subcategory_slug')
        if subcategory_slug == 'reklamnyj-rolik':
            return ServiceAdClipRequestForm
        elif subcategory_slug == 'reklamnaya-muzyka':
            return ServiceAdMusicRequestForm
        return None

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = ServiceAdvertisement.objects.all()
            subcategory_slug = self.kwargs.get('subcategory_slug', None)
            if subcategory_slug:
                try:
                    subcategory = getattr(Subcategory.objects.get(slug=subcategory_slug), 'id')
                    queryset = queryset.filter(subcategory=subcategory)
                except Subcategory.DoesNotExist:
                    HttpResponseNotFound()
            else:
                queryset = queryset.none()
            return queryset

    def get_success_url(self):
        return reverse('musprivet:ads_list', kwargs={'subcategory_slug': self.kwargs.get('subcategory_slug')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'audioreklama'
        category = get_object_or_404(Category, slug=category_url)
        subcategory_slug = self.kwargs.get('subcategory_slug', None)
        context['subcategory_slug'] = subcategory_slug
        context['categories'] = Category.objects.all()
        context['video_ads'] = ServiceVideoAdvertisement.objects.all()
        context['rolik_prices'] = ServiceAdClipPrice.objects.filter(type='R')
        context['script_prices'] = ServiceAdClipPrice.objects.filter(type='S')
        context['music_prices'] = ServiceAdClipPrice.objects.filter(type='M')
        context['reviews'] = Review.objects.filter(category=category)
        if subcategory_slug:
            try:
                subcategory = getattr(Subcategory.objects.get(slug=subcategory_slug), 'id')
                subcategory_name = Subcategory.objects.get(slug=subcategory_slug)
                context['tags'] = Tag.objects.filter(subcategory=subcategory)
                if subcategory_name:
                    context['description'] = 'Услуги для бизнеса: ' + category.name + ' ' + subcategory_name.name + \
                                             ' Под ключ с адаптацией в любой хронометраж за 5 дней!'
                else:
                    context['description'] = 'Услуги для бизнеса: ' + category.name + ' ' + ' Под ключ с адаптацией в ' \
                                                                                            'любой хронометраж за 5 дней!'
            except Subcategory.DoesNotExist:
                HttpResponseNotFound()
        else:
            context['tags'] = Tag.objects.filter(category=category)
        context['form'] = self.get_form_class()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:ads_list',
                                                                 kwargs={'subcategory_slug':
                                                                             self.kwargs.get('subcategory_slug')}))
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class AdvertisementView(TemplateView):
    template_name = 'musprivet/audioreklama.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_url = 'audioreklama'
        category = get_object_or_404(Category, slug=category_url)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:audioreklama'))
        context['description'] = 'Услуги для бизнеса: ' + category.name + ' ' + ' Под ключ с адаптацией в ' \
                                                                                'любой хронометраж за 5 дней!'
        if category.image == None:
            context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        else:
            image_url = category.image.url
            context['image'] = self.request.build_absolute_uri(image_url)
        return context


class AboutUsView(TemplateView):
    template_name = 'musprivet/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:about_us'))
        context['description'] = 'Продюсерский центр «Музпривет» — творческое содружество композиторов, ' \
                                 'авторов текстов, исполнителей, актёров, режиссёров и продюсеров, работающих ' \
                                 'в сферах рекламы, радио, телевидения и кинематографе.'
        context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        return context


class UserManualView(TemplateView):
    template_name = 'musprivet/user_manual.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:user_manual'))
        context['description'] = 'Договор на оказание услуг (публичная оферта)'
        context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        return context


class RefundView(TemplateView):
    template_name = 'musprivet/refund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['title'] = 'Готовые музыкальные поздравления и песни на заказ в подарок для ваших любимых от Музпривет.'
        context['url'] = self.request.build_absolute_uri(reverse('musprivet:refund'))
        context['description'] = 'Способы оплаты и правила возврата денежных средств'
        context['image'] = self.request.build_absolute_uri(static('img/mainicon.png'))
        return context










