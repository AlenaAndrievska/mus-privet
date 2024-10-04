from django.db import models


class Category(models.Model):
    """Модель категории услуг"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    slug = models.CharField(max_length=100, db_index=True, verbose_name='slug')

    class Meta:
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.name}'


class Subcategory(models.Model):
    """Модель подкатегории услуг"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, related_name='subcategory')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, default=None, verbose_name='URL')

    class Meta:
        db_table = 'subcategory'
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='tags', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, related_name='sub_tags', on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    is_male_name_related = models.BooleanField(default=False)
    is_female_name_related = models.BooleanField(default=False)

    class Meta:
        db_table = 'tag'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

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

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        ordering = ['name']
        db_table = 'name'
        verbose_name = 'имя'
        verbose_name_plural = 'имена'

    def __str__(self):
        return self.name


class ServiceCongratsByTag(models.Model):
    """Модель музыкальных поздравлений по тегу"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='services_by_tag_congrats', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)

    class Meta:
        db_table = 'service_by_tag'
        verbose_name = 'поздравление по тегу'
        verbose_name_plural = 'поздравления по тегу'

    def __str__(self):
        return self.title


class PoemByName(models.Model):
    """Модель стихов для поздравлений по именам"""
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    name = models.ForeignKey(Name, on_delete=models.CASCADE)

    class Meta:
        db_table = 'poem_by_name'
        verbose_name = 'стих по имени'
        verbose_name_plural = 'стихи по именам'

    def __str__(self):
        return self.title


class ServiceCongratsByName(models.Model):
    """Модель музыкальных поздравлений по имени"""
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='services_by_name_congrats', on_delete=models.CASCADE)
    poem = models.ForeignKey(PoemByName, null=True, blank=True, on_delete=models.CASCADE, max_length=100, related_name='audio')
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)

    class Meta:
        db_table = 'service_by_name'
        verbose_name = 'поздравление по имени'
        verbose_name_plural = 'поздравления по имени'

    def __str__(self):
        return self.title


class Blog(models.Model):
    """Модель статей для блога"""
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    date_field = models.DateField()
    image_field = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        db_table = 'blog'
        verbose_name = 'статья блога'
        verbose_name_plural = 'статьи блога'

    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    city = models.CharField(max_length=100, db_index=True, verbose_name='city', null=True, blank=True)
    text = models.TextField(verbose_name='text')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, related_name='review', default=None)

    class Meta:
        db_table = 'review'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.name

class ServiceSongs(models.Model):
    """Модель песен аудио формата"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='services_songs', on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to='images/', null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)

    class Meta:
        db_table = 'song'
        verbose_name = 'песня'
        verbose_name_plural = 'песни'

    def __str__(self):
        return self.title


class ServiceSongsVideo(models.Model):
    """Модель песен видео формата"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='services_video_songs', on_delete=models.CASCADE)
    video_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'video song'
        verbose_name = 'видео песня'
        verbose_name_plural = 'видео песни'

    def __str__(self):
        return self.title


class SongRequest(models.Model):
    """Модель заявок на песни"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'song request'
        verbose_name = 'заявка на песню'
        verbose_name_plural = 'заявки на песни'

    def __str__(self):
        return self.name


class ServiceAdvertisement(models.Model):
    """Модель аудиорекламы"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, related_name='sub_ads', on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)

    class Meta:
        db_table = 'advertisement'
        verbose_name = 'реклама'
        verbose_name_plural = 'реклама'

    def __str__(self):
        return self.title


class ServiceVideoAdvertisement(models.Model):
    """Модель аудиорекламы видео-формата"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'video-advertisement'
        verbose_name = 'видео реклама'
        verbose_name_plural = 'видео реклама'

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
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    timing = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255)

    class Meta:
        db_table = 'ad_clip_price'
        verbose_name = 'цена'
        verbose_name_plural = 'цены'

    def __str__(self):
        return self.title


class ServiceAdClipRequest(models.Model):
    """Модель заявок на рекламные ролики и сценарии"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service = models.ForeignKey(ServiceAdClipPrice, on_delete=models.CASCADE)
    timing = models.CharField(max_length=255, blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clip request'
        verbose_name = 'заявка на рекламный ролик'
        verbose_name_plural = 'заявки на рекламные ролики'

    def __str__(self):
        return self.name


class ServiceAdMusicRequest(models.Model):
    """Модель заявок на рекламную музыку"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service = models.ForeignKey(ServiceAdClipPrice, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'music request'
        verbose_name = 'заявка на рекламную музыку'
        verbose_name_plural = 'заявки на рекламную музыку'

    def __str__(self):
        return self.name

class PaymentService(models.Model):
    service = models.ForeignKey(ServiceCongratsByTag, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    congratulation = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PaymentService'
        verbose_name = 'оплата услуги'
        verbose_name_plural = 'оплата услуги'

    def __str__(self):
        return f"Payment for {self.service.title} by {self.email}"


class PaymentServiceByName(models.Model):
    service = models.ForeignKey(ServiceCongratsByName, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    congratulation = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PaymentServiceByName'
        verbose_name = 'оплата услуги по имени'
        verbose_name_plural = 'оплата услуги по имени'

    def __str__(self):
        return f"Payment for {self.service.title} by {self.email}"











