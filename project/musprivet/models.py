from django.db import models


class Category(models.Model):
    """Модель категории услуг"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='название')
    slug = models.CharField(max_length=100, db_index=True, verbose_name='слаг')
    image = models.ImageField(upload_to='images/', null=True, blank=True, default=None, verbose_name='картинка (опционально)')

    class Meta:
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = '1.1. Таблица категорий'

    def __str__(self):
        return f'{self.name}'


class Subcategory(models.Model):
    """Модель подкатегории услуг"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, related_name='subcategory',
                                 verbose_name='категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, default=None, verbose_name='слаг (автоматически)')

    class Meta:
        db_table = 'subcategory'
        verbose_name = 'подкатегория'
        verbose_name_plural = '1.2. Таблица подкатегорий'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(max_length=255, verbose_name='название')
    category = models.ForeignKey(Category, related_name='tags', on_delete=models.CASCADE, verbose_name='категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='слаг (автоматически)')
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, related_name='sub_tags',
                                    on_delete=models.CASCADE, verbose_name='подкатегория (если есть)')
    number = models.IntegerField(null=True, blank=True,
                                 verbose_name='номер (для тегов Аудиорекламы, номер означает каким по счету '
                                              'тег будет на странице)')
    is_male_name_related = models.BooleanField(default=False, verbose_name='привязан ли к тегу список мужских имен')
    is_female_name_related = models.BooleanField(default=False, verbose_name='привязан ли к тегу список женских имен')

    class Meta:
        db_table = 'tag'
        verbose_name = 'тег'
        verbose_name_plural = '2.1. Таблица тегов'

    def __str__(self):
        return self.name


class Name(models.Model):
    """Модель имен"""
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    name = models.CharField(max_length=100, verbose_name='имя')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='пол')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='слаг (автоматически)')

    class Meta:
        ordering = ['name']
        db_table = 'name'
        verbose_name = 'имя'
        verbose_name_plural = '2.2. Таблица имен'

    def __str__(self):
        return self.name


class ServiceCongratsByTag(models.Model):
    """Модель музыкальных поздравлений по тегу"""
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='текст поздравления (опционально)')
    category = models.ForeignKey(Category, related_name='services_by_tag_congrats', on_delete=models.CASCADE,
                                 verbose_name='категория (музыкальное поздравление)')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тег')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='слаг (автоматически)')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')

    class Meta:
        db_table = 'service_by_tag'
        verbose_name = 'поздравление по тегу'
        verbose_name_plural = '2.3. Таблица поздравлений по тегу'

    def __str__(self):
        return self.title


class PoemByName(models.Model):
    """Модель стихов для поздравлений по именам"""
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='название')
    text = models.TextField(verbose_name='текст стихотворения')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тег')
    name = models.ForeignKey(Name, on_delete=models.CASCADE, verbose_name='имя')

    class Meta:
        db_table = 'poem_by_name'
        verbose_name = 'стих по имени'
        verbose_name_plural = '2.4. Таблица стихов по именам'

    def __str__(self):
        return self.title


class ServiceCongratsByName(models.Model):
    """Модель музыкальных поздравлений по имени"""
    title = models.CharField(max_length=255, verbose_name='название')
    category = models.ForeignKey(Category, related_name='services_by_name_congrats', on_delete=models.CASCADE,
                                 verbose_name='категория (музыкальное поздравление)')
    poem = models.ForeignKey(PoemByName, null=True, blank=True, on_delete=models.CASCADE, max_length=100, related_name='audio',
                             verbose_name='стихотворение')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')

    class Meta:
        db_table = 'service_by_name'
        verbose_name = 'поздравление по имени'
        verbose_name_plural = '2.5. Таблица поздравлений по именам'

    def __str__(self):
        return self.title


class Blog(models.Model):
    """Модель статей для блога"""
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='название')
    text = models.TextField(verbose_name='текст')
    date_field = models.DateField()
    image_field = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='картинка')

    class Meta:
        db_table = 'blog'
        verbose_name = 'статья блога'
        verbose_name_plural = '3. Таблица блога'

    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='имя пользователя')
    city = models.CharField(max_length=100, db_index=True, null=True, blank=True, verbose_name='город')
    text = models.TextField(verbose_name='текст отзыва')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, related_name='review',
                                 default=None, verbose_name='категория')

    class Meta:
        db_table = 'review'
        verbose_name = 'отзыв'
        verbose_name_plural = '4. Таблица отзывов'

    def __str__(self):
        return self.name

class ServiceSongs(models.Model):
    """Модель песен аудио формата"""
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание (опционально)')
    category = models.ForeignKey(Category, related_name='services_songs', on_delete=models.CASCADE,
                                 verbose_name='категория')
    image_field = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='картинка')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')

    class Meta:
        db_table = 'song'
        verbose_name = 'песня'
        verbose_name_plural = '5.1. Таблица песен'

    def __str__(self):
        return self.title


class ServiceSongsVideo(models.Model):
    """Модель песен видео формата"""
    VERTICAL = 'V'
    HORIZONTAL = 'H'
    TYPE_CHOICES = [
        (VERTICAL, 'вертикальный'),
        (HORIZONTAL, 'горизонтальный'),
    ]
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание (опционально)')
    category = models.ForeignKey(Category, related_name='services_video_songs', on_delete=models.CASCADE,
                                 verbose_name='категория')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=True, null=True, verbose_name='выберите тип видео')
    video_url = models.URLField(blank=True, null=True, verbose_name='ссылка на видео')

    class Meta:
        db_table = 'video song'
        verbose_name = 'видео песня'
        verbose_name_plural = '5.2. Таблица песен в формате видео'

    def __str__(self):
        return self.title


class SongRequest(models.Model):
    """Модель заявок на песни"""
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='электронная почта')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата заявки')

    class Meta:
        db_table = 'song request'
        verbose_name = 'заявка на песню'
        verbose_name_plural = 'Форма заявки на песню'

    def __str__(self):
        return self.name


class ServiceAdvertisement(models.Model):
    """Модель аудиорекламы"""
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тег')
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, related_name='sub_ads',
                                    on_delete=models.CASCADE, verbose_name='подкатегория')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')

    class Meta:
        db_table = 'advertisement'
        verbose_name = 'реклама'
        verbose_name_plural = '6.1. Таблица аудиорекламы'

    def __str__(self):
        return self.title


class ServiceVideoAdvertisement(models.Model):
    """Модель аудиорекламы видео-формата"""
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание (опционально)')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тег')
    video_url = models.URLField(null=True, blank=True, verbose_name='ссылка на видео')

    class Meta:
        db_table = 'video-advertisement'
        verbose_name = 'видео реклама'
        verbose_name_plural = '6.2. Таблица аудиорекламы в формате видео'

    def __str__(self):
        return self.title


class ServiceAdClipPrice(models.Model):
    """Модель цен на рекламные роли и сценарии"""
    ROLIK = 'R'
    SCRIPT = 'S'
    MUSIC = 'M'
    CONGRAT = 'C'
    TYPE_CHOICES = [
        (ROLIK, 'Аудиоролик'),
        (SCRIPT, 'Сценарий'),
        (MUSIC, 'Музыка'),
        (CONGRAT, 'Музыкальное поздравление')
    ]
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание (каждый пункт с новой строки)')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, verbose_name='выберите тип')
    timing = models.CharField(max_length=255, blank=True, null=True, verbose_name='хронометраж (опционально)')
    price = models.CharField(max_length=255, verbose_name='цена (целое число)')

    class Meta:
        db_table = 'ad_clip_price'
        verbose_name = 'цена'
        verbose_name_plural = '7. Таблица цен на услуги аудиорекламы и поздравлений'

    def __str__(self):
        return self.title


class ServiceAdClipRequest(models.Model):
    """Модель заявок на рекламные ролики и сценарии"""
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='электронная почта')
    service = models.ForeignKey(ServiceAdClipPrice, on_delete=models.CASCADE, verbose_name='услуга')
    timing = models.CharField(max_length=255, blank=True, null=True, verbose_name='хронометраж')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата заявки')

    class Meta:
        db_table = 'clip request'
        verbose_name = 'заявка на рекламный ролик'
        verbose_name_plural = 'Форма заявки на рекламные ролики и сценарии'

    def __str__(self):
        return self.name


class ServiceAdMusicRequest(models.Model):
    """Модель заявок на рекламную музыку"""
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='электронная почта')
    service = models.ForeignKey(ServiceAdClipPrice, on_delete=models.CASCADE, verbose_name='услуга')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name='аудио файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата заявки')

    class Meta:
        db_table = 'music request'
        verbose_name = 'заявка на рекламную музыку'
        verbose_name_plural = 'Форма заявки на рекламную музыку'

    def __str__(self):
        return self.name

class PaymentService(models.Model):
    service = models.ForeignKey(ServiceCongratsByTag, on_delete=models.CASCADE, verbose_name='услуга')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='электронная почта')
    congratulation = models.TextField(blank=True, null=True, verbose_name='текст поздравления')
    price = models.IntegerField(blank=True, null=True, verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время оплаты')

    class Meta:
        db_table = 'PaymentService'
        verbose_name = 'оплата услуги'
        verbose_name_plural = 'Форма оплаты услуги музыкального поздравления по тегу'

    def __str__(self):
        return f"Payment for {self.service.title} by {self.email}"


class PaymentServiceByName(models.Model):
    service = models.ForeignKey(ServiceCongratsByName, on_delete=models.CASCADE, verbose_name='услуга')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='электронная почта')
    congratulation = models.TextField(blank=True, null=True, verbose_name='текст поздравления')
    price = models.IntegerField(blank=True, null=True, verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время оплаты')

    class Meta:
        db_table = 'PaymentServiceByName'
        verbose_name = 'оплата услуги по имени'
        verbose_name_plural = 'Форма оплаты услуги музыкального поздравления по имени'

    def __str__(self):
        return f"Payment for {self.service.title} by {self.email}"











