from django.test import TestCase
from django.urls import reverse

from .forms import PaymentForm1, PaymentForm2, SongRequestForm, ServiceAdClipRequestForm, ServiceAdMusicRequestForm
from .models import ServiceCongratsByTag, Tag, Category, Subcategory, Blog, Review, Name, ServiceAdClipPrice, \
    PaymentService, PoemByName, ServiceCongratsByName, ServiceSongs, ServiceSongsVideo, ServiceAdvertisement, \
    ServiceVideoAdvertisement


class ServiceCongratsByTagListViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(slug='mus-pozdrav')
        self.subcategory = Subcategory.objects.create(slug='sub-categor', category=self.category)
        self.tag1 = Tag.objects.create(name='Тестовый тег', slug='test-slug', category=self.category)
        self.tag2 = Tag.objects.create(name='Поздравление жене по имени', slug='pozdravlenie-zhene-po-imeni', category=self.category)
        self.congrat1 = ServiceCongratsByTag.objects.create(category=self.category, tag=self.tag1, slug='congrat_1',
                                                            audio_file='test1.mp3')
        self.congrat2 = ServiceCongratsByTag.objects.create(category=self.category, tag=self.tag2, slug='congrat_2',
                                                            audio_file='test2.mp3')
        self.congrat3 = ServiceCongratsByTag.objects.create(category=self.category, tag=self.tag1, slug='congrat_3',
                                                            audio_file='test2.mp3')
        self.article1 = Blog.objects.create(title='article1', date_field='2024-01-01', image_field='image.png')
        self.review1 = Review.objects.create(name='User', category=self.category)


    def test_view_with_valid_tag_slug(self):
        response = self.client.get(reverse('musprivet:congrat_list', kwargs={'tag_slug': self.tag1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('congrats', response.context)
        self.assertQuerysetEqual(response.context['congrats'].values_list('id', flat=True),
                                 [self.congrat1.id, self.congrat3.id], ordered=False)

    def test_view_with_invalid_tag_slug(self):
        response = self.client.get(reverse('musprivet:congrat_list', kwargs={'tag_slug': 'tag'}))
        self.assertEqual(response.status_code, 404)

    def test_view_with_no_slug(self):
        response = self.client.get(reverse('musprivet:congrat_list_default'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('congrats', response.context)
        self.assertQuerysetEqual(response.context['congrats'], [])

    def test_context_data_with_valid_slug(self):
        response = self.client.get(reverse('musprivet:congrat_list', kwargs={'tag_slug': self.tag1.slug}))
        self.assertIn('categories', response.context)
        self.assertIn('subcategories', response.context)
        self.assertIn('tags', response.context)
        self.assertIn('articles', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('grouped_names', response.context)
        self.assertIn('current_tag', response.context)
        self.assertEqual(response.context['current_tag'], self.tag1)
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertQuerysetEqual(response.context['subcategories'], [self.subcategory])
        self.assertQuerysetEqual(response.context['articles'], [self.article1])
        self.assertQuerysetEqual(response.context['reviews'], [self.review1])

    def test_context_data_with_no_slug(self):
        response = self.client.get(reverse('musprivet:congrat_list_default'))
        self.assertIn('grouped_names', response.context)
        self.assertIn('current_tag', response.context)
        self.assertEqual(response.context['current_tag'].slug,
                         'pozdravlenie-zhene-po-imeni')


class ServiceCongratsByTagDetailViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(slug='mus-pozdrav')
        self.subcategory = Subcategory.objects.create(slug='sub-categor', category=self.category)
        self.tag1 = Tag.objects.create(name='Тестовый тег', slug='test-slug', category=self.category)
        self.congrat = ServiceCongratsByTag.objects.create(category=self.category, tag=self.tag1, slug='congrat_1',
                                                            audio_file='test1.mp3')
        self.price = ServiceAdClipPrice.objects.create(title='price1', type='C', price='400')

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('musprivet:congrat_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'congrat_slug': self.congrat.slug}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        response = self.client.get(reverse('musprivet:congrat_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'congrat_slug': self.congrat.slug}))
        self.assertTemplateUsed(response, 'musprivet/congrat_detail.html')

    def test_detail_view_context(self):
        response = self.client.get(reverse('musprivet:congrat_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'congrat_slug': self.congrat.slug}))
        self.assertIn('current_tag', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('form', response.context)
        self.assertIn('price', response.context)
        self.assertEqual(response.context['current_tag'], self.tag1)
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertEqual(response.context['price'], self.price)

    def test_form_valid_data(self):
        form_data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'congratulation': 'Happy Birthday!'
        }
        form = PaymentForm1(data=form_data)
        form.instance.service = self.congrat
        form.instance.price = int(self.price.price)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '1234567890')
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')
        self.assertEqual(form.cleaned_data['congratulation'], 'Happy Birthday!')

    def test_form_invalid_data(self):
        form_data = {
            'phone': '',
            'email': 'invalid-email',
            'congratulation': ''
        }
        form = PaymentForm1(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)


    def test_form_save(self):
        form_data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'congratulation': 'Happy Birthday!'
        }
        form = PaymentForm1(data=form_data)
        form.instance.service = self.congrat
        form.instance.price = int(self.price.price)
        self.assertTrue(form.is_valid())
        payment_service = form.save()
        self.assertEqual(payment_service.phone, '1234567890')
        self.assertEqual(payment_service.email, 'test@example.com')
        self.assertEqual(payment_service.congratulation, 'Happy Birthday!')
        self.assertEqual(payment_service.service, self.congrat)
        self.assertEqual(payment_service.price, 400)


    def test_form_empty_data(self):
        form = PaymentForm1(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)


class PoemByNameDetailViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(slug='mus-pozdrav')
        self.subcategory = Subcategory.objects.create(slug='sub-categor', category=self.category)
        self.tag1 = Tag.objects.create(name='Тестовый тег', slug='test-slug', category=self.category)
        self.name1 = Name.objects.create(name='A', slug='a-name', gender='M')
        self.name2 = Name.objects.create(name='Ab', slug='ab-name', gender='M')
        self.name3 = Name.objects.create(name='B', slug='b-name', gender='M')
        self.name4 = Name.objects.create(name='C', slug='c-name', gender='F')
        self.name5 = Name.objects.create(name='D', slug='d-name', gender='F')
        self.poem1 = PoemByName.objects.create(title='title1', name=self.name1, tag=self.tag1)
        self.poem2 = PoemByName.objects.create(title='title2', name=self.name2, tag=self.tag1)
        self.poem3 = PoemByName.objects.create(title='title3', name=self.name3, tag=self.tag1)
        self.poem4 = PoemByName.objects.create(title='title4', name=self.name4, tag=self.tag1)
        self.poem5 = PoemByName.objects.create(title='title5', name=self.name5, tag=self.tag1)
        self.congrat1 = ServiceCongratsByName.objects.create(category=self.category, title='congrat1', poem=self.poem1,
                                                            audio_file='file1.mp3')
        self.congrat2 = ServiceCongratsByName.objects.create(category=self.category, title='congrat2', poem=self.poem3,
                                                            audio_file='file2.mp3')
        self.congrat3 = ServiceCongratsByName.objects.create(category=self.category, title='congrat3', poem=self.poem3,
                                                            audio_file='file3.mp3')
        self.congrat4 = ServiceCongratsByName.objects.create(category=self.category, title='congrat4', poem=self.poem2,
                                                            audio_file='file4.mp3')
        self.congrat5 = ServiceCongratsByName.objects.create(category=self.category, title='congrat5', poem=self.poem3,
                                                            audio_file='file5.mp3')
        self.price = ServiceAdClipPrice.objects.create(title='price1', type='C', price='400')

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('musprivet:name_poem_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'name_slug': self.name1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        response = self.client.get(reverse('musprivet:name_poem_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'name_slug': self.name1.slug}))
        self.assertTemplateUsed(response, 'musprivet/name_poem_detail.html')

    def test_detail_view_context(self):
        response = self.client.get(reverse('musprivet:name_poem_detail', kwargs={'tag_slug': self.tag1.slug,
                                                                     'name_slug': self.name3.slug}))
        self.assertIn('current_tag', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('form', response.context)
        self.assertIn('name_congrats', response.context)
        self.assertIn('price', response.context)
        self.assertEqual(response.context['current_tag'], self.tag1)
        self.assertEqual(response.context['price'], self.price)
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertQuerysetEqual(response.context['name_congrats'],
                                 [self.congrat2, self.congrat3, self.congrat5], ordered=False)

    def test_form_valid_data(self):
        form_data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'congratulation': 'Happy Birthday!',
            'service': self.congrat1.id
        }
        form = PaymentForm2(data=form_data)
        form.instance.price = int(self.price.price)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '1234567890')
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')
        self.assertEqual(form.cleaned_data['congratulation'], 'Happy Birthday!')

    def test_form_invalid_data(self):
        form_data = {
            'phone': '',
            'email': 'invalid-email',
            'congratulation': ''
        }
        form = PaymentForm2(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)

    def test_form_save(self):
        form_data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'congratulation': 'Happy Birthday!',
            'service': self.congrat1.id
        }
        form = PaymentForm2(data=form_data)
        form.instance.price = int(self.price.price)
        self.assertTrue(form.is_valid())
        payment_service = form.save()
        self.assertEqual(payment_service.phone, '1234567890')
        self.assertEqual(payment_service.email, 'test@example.com')
        self.assertEqual(payment_service.congratulation, 'Happy Birthday!')
        self.assertEqual(payment_service.service, self.congrat1)
        self.assertEqual(payment_service.price, 400)

    def test_form_empty_data(self):
        form = PaymentForm2(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)


class ServiceSongsListViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(slug='podarit-pesnu')
        self.subcategory = Subcategory.objects.create(slug='sub-categor', category=self.category)
        self.song1 = ServiceSongs.objects.create(category=self.category, title='song1', image_field='file1.png',
                                                            audio_file='file1.mp3')
        self.song2 = ServiceSongs.objects.create(category=self.category, title='song2', image_field='file2.png',
                                                            audio_file='file2.mp3')
        self.videosong2 = ServiceSongsVideo.objects.create(category=self.category, title='song2',
                                                            video_url='video.com')

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('musprivet:song_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        response = self.client.get(reverse('musprivet:song_list'))
        self.assertTemplateUsed(response, 'musprivet/song_list.html')

    def test_detail_view_context(self):
        response = self.client.get(reverse('musprivet:song_list'))
        self.assertIn('categories', response.context)
        self.assertIn('form', response.context)
        self.assertIn('video_songs', response.context)
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertQuerysetEqual(response.context['video_songs'], [self.videosong2])

    def test_form_valid_data(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'message': 'Message',
        }
        form = SongRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Ivan')
        self.assertEqual(form.cleaned_data['phone'], '1234567890')
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')
        self.assertEqual(form.cleaned_data['message'], 'Message')

    def test_form_invalid_data(self):
        form_data = {
            'name': '',
            'phone': '',
            'email': 'invalid-email',
            'message': 'Message',
        }
        form = SongRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)

    def test_form_save(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'message': 'Message',
        }
        form = SongRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
        payment_service = form.save()
        self.assertEqual(payment_service.name, 'Ivan')
        self.assertEqual(payment_service.phone, '1234567890')
        self.assertEqual(payment_service.email, 'test@example.com')
        self.assertEqual(payment_service.message, 'Message')


    def test_form_empty_data(self):
        form = SongRequestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)


class ServiceAdvertisementListViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Аудиореклама', slug='audioreklama')
        self.subcategory1 = Subcategory.objects.create(name='Рекламный ролик', slug='reklamnyj-rolik', category=self.category)
        self.subcategory2 = Subcategory.objects.create(name='Рекламная музыка', slug='reklamnaya-muzyka', category=self.category)
        self.tag1 = Tag.objects.create(name='Музыкальные ролики', slug='muzykalnye-roliki', category=self.category,
                                       subcategory=self.subcategory1, number=1)
        self.tag2 = Tag.objects.create(name='Игровые ролики', slug='igrovye-roliki', category=self.category,
                                       subcategory=self.subcategory1, number=2)
        self.review1 = Review.objects.create(name='User', category=self.category)
        self.ad1 = ServiceAdvertisement.objects.create(subcategory=self.subcategory1, title='ad1', tag=self.tag1,
                                                      description='Описание', audio_file='file1.mp3')
        self.ad2 = ServiceAdvertisement.objects.create(subcategory=self.subcategory1, title='ad2', tag=self.tag1,
                                                      description='Описание', audio_file='file2.mp3')
        self.ad3 = ServiceAdvertisement.objects.create(subcategory=self.subcategory1, title='ad3', tag=self.tag2,
                                                      description='Описание', audio_file='file3.mp3')
        self.videoad1 = ServiceVideoAdvertisement.objects.create(title='ad4', tag=self.tag1, video_url='video1.com',
                                                                 description='Описание')
        self.price1 = ServiceAdClipPrice.objects.create(title='price1', type='R', description='Описание')
        self.price2 = ServiceAdClipPrice.objects.create(title='price2', type='S', description='Описание')
        self.price3 = ServiceAdClipPrice.objects.create(title='price3', type='M', description='Описание')

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('musprivet:ads_list', kwargs={'subcategory_slug': self.subcategory1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        response = self.client.get(reverse('musprivet:ads_list', kwargs={'subcategory_slug': self.subcategory1.slug}))
        self.assertTemplateUsed(response, 'musprivet/ads_list.html')

    def test_detail_view_context(self):
        response = self.client.get(reverse('musprivet:ads_list', kwargs={'subcategory_slug': self.subcategory1.slug}))
        self.assertIn('categories', response.context)
        self.assertIn('form', response.context)
        self.assertIn('subcategory_slug', response.context)
        self.assertIn('video_ads', response.context)
        self.assertIn('rolik_prices', response.context)
        self.assertIn('script_prices', response.context)
        self.assertIn('music_prices', response.context)
        self.assertIn('reviews', response.context)
        self.assertIn('tags', response.context)
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertQuerysetEqual(response.context['subcategory_slug'], self.subcategory1.slug)
        self.assertQuerysetEqual(response.context['video_ads'], [self.videoad1])
        self.assertQuerysetEqual(response.context['rolik_prices'], [self.price1])
        self.assertQuerysetEqual(response.context['script_prices'], [self.price2])
        self.assertQuerysetEqual(response.context['music_prices'], [self.price3])
        self.assertQuerysetEqual(response.context['reviews'], [self.review1])
        self.assertQuerysetEqual(response.context['tags'], [self.tag1, self.tag2], ordered=False)

    def test_form_valid_data(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'timing': '30 секунд',
            'service': self.price1
        }
        form = ServiceAdClipRequestForm(data=form_data)
        request = form.save()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Ivan')
        self.assertEqual(form.cleaned_data['phone'], '1234567890')
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')
        self.assertEqual(form.cleaned_data['timing'], '30 секунд')
        self.assertEqual(request.service, self.price1)

    def test_form2_valid_data(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'service': self.price3
        }
        form = ServiceAdMusicRequestForm(data=form_data)
        request = form.save()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Ivan')
        self.assertEqual(form.cleaned_data['phone'], '1234567890')
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')
        self.assertEqual(request.service, self.price3)

    def test_form_invalid_data(self):
        form_data = {
            'name': '',
            'phone': '',
            'email': 'invalid-email',
        }
        form = ServiceAdClipRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)

    def test_form2_invalid_data(self):
        form_data = {
            'name': '',
            'phone': '',
            'email': 'invalid-email',
        }
        form = ServiceAdMusicRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)

    def test_form_save(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'timing': '30 секунд',
            'service': self.price1
        }
        form = ServiceAdClipRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
        request_service = form.save()
        self.assertEqual(request_service.name, 'Ivan')
        self.assertEqual(request_service.phone, '1234567890')
        self.assertEqual(request_service.email, 'test@example.com')
        self.assertEqual(request_service.timing, '30 секунд')
        self.assertEqual(request_service.service, self.price1)

    def test_form2_save(self):
        form_data = {
            'name': 'Ivan',
            'phone': '1234567890',
            'email': 'test@example.com',
            'service': self.price3
        }
        form = ServiceAdMusicRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
        request_service = form.save()
        self.assertEqual(request_service.name, 'Ivan')
        self.assertEqual(request_service.phone, '1234567890')
        self.assertEqual(request_service.email, 'test@example.com')
        self.assertEqual(request_service.service, self.price3)


    def test_form_empty_data(self):
        form = ServiceAdClipRequestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('service', form.errors)

    def test_form2_empty_data(self):
        form = ServiceAdMusicRequestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('service', form.errors)











