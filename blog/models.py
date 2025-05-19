from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Alt Kategori Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Ana Kategori")
    description = models.TextField(blank=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Alt Kategori"
        verbose_name_plural = "Alt Kategoriler"
        ordering = ['category', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class BlogPost(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Resim", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="Kategori")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="Alt Kategori")
    tags = models.ManyToManyField('Tag', related_name='blog_tags', blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Education(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Bölüm")
    school = models.CharField(max_length=200, verbose_name="Okul")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    is_current = models.BooleanField(default=False, verbose_name="Devam Ediyor")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="GPA")
    description = models.TextField(verbose_name="Açıklama")
    tags = models.ManyToManyField('Tag', related_name='education_tags', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Eğitim"
        verbose_name_plural = "Eğitimler"
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.school}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.school}"

class Experience(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Pozisyon")
    company = models.CharField(max_length=200, verbose_name="Şirket")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    is_current = models.BooleanField(default=False, verbose_name="Devam Ediyor")
    description = models.TextField(verbose_name="Açıklama")
    tags = models.ManyToManyField('Tag', related_name='experience_tags', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Deneyim"
        verbose_name_plural = "Deneyimler"
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"

class Certificate(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Sertifika Adı")
    issuer = models.CharField(max_length=200, verbose_name="Veren Kurum")
    date = models.DateField(verbose_name="Tarih")
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    credential_url = models.URLField(verbose_name="Sertifika Linki", blank=True, null=True)
    credential_id = models.CharField(max_length=100, verbose_name="Sertifika ID", blank=True, null=True)
    image = models.ImageField(upload_to='certificates/', verbose_name="Sertifika Görseli", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Sertifika"
        verbose_name_plural = "Sertifikalar"
        ordering = ['-date', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.issuer}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Proje Kategorisi"
        verbose_name_plural = "Proje Kategorileri"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Proje Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Açıklama")
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects', verbose_name="Kategori")
    image = models.ImageField(upload_to='projects/', verbose_name="Proje Görseli")
    project_url = models.URLField(verbose_name="Proje Linki", blank=True)
    github_url = models.URLField(verbose_name="GitHub Linki", blank=True)
    tags = models.ManyToManyField('Tag', related_name='project_tags')
    button_text = models.CharField(max_length=50, verbose_name="Buton Metni", default="Detayları Gör")
    button_url = models.URLField(verbose_name="Buton Linki (opsiyonel)", blank=True)

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
        ordering = ['name']

class CodeLanguage(models.Model):
    name = models.CharField(max_length=50, verbose_name="Dil Adı")
    icon = models.CharField(max_length=50, verbose_name="İkon Sınıfı (opsiyonel)", blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = "Kod Dili"
        verbose_name_plural = "Kod Dilleri"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CodeCategory(models.Model):
    language = models.ForeignKey('CodeLanguage', on_delete=models.CASCADE, related_name='categories', verbose_name="Programlama Dili", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = "Kod Kategorisi"
        verbose_name_plural = "Kod Kategorileri"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.language.name} - {self.name}" if self.language else self.name

class CodeExample(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    language = models.ForeignKey(CodeLanguage, on_delete=models.CASCADE, related_name="code_examples", verbose_name="Programlama Dili")
    category = models.ForeignKey(CodeCategory, on_delete=models.CASCADE, related_name="code_examples", verbose_name="Kategori")
    code = models.TextField(verbose_name="Kod")
    description = models.TextField(verbose_name="Açıklama")
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Kod Örneği"
        verbose_name_plural = "Kod Örnekleri"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.language.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.language.name}"

class About(models.Model):
    profile_image = models.ImageField(upload_to='about/', verbose_name='Profil Fotoğrafı')
    full_name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    title = models.CharField(max_length=100, verbose_name='Ünvan')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    address = models.CharField(max_length=150, verbose_name='Adres')

    def __str__(self):
        return self.full_name

class ContactInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    email = models.EmailField(verbose_name="E-posta", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Adres", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")

    class Meta:
        ordering = ['order']
        verbose_name = "İletişim Bilgisi"
        verbose_name_plural = "İletişim Bilgileri"

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="Site Adı")
    logo = models.ImageField(upload_to='site/', verbose_name="Logo", blank=True, null=True)
    footer_text = models.CharField(max_length=255, verbose_name="Footer Yazısı", blank=True)
    github = models.URLField(verbose_name="GitHub", blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn", blank=True)
    twitter = models.URLField(verbose_name="Twitter", blank=True)
    instagram = models.URLField(verbose_name="Instagram", blank=True)
    cv_file = models.FileField(upload_to='cv/', verbose_name="CV Dosyası", blank=True, null=True)
    copyright = models.CharField(max_length=255, verbose_name="Copyright", blank=True)
    contact_title = models.CharField(max_length=100, verbose_name="İletişim Başlığı", default="İletişim")
    contact_subtitle = models.TextField(verbose_name="İletişim Alt Başlığı", blank=True, null=True)
    contact_form_title = models.CharField(max_length=100, verbose_name="Form Başlığı", default="Bana Ulaşın")
    contact_form_subtitle = models.TextField(verbose_name="Form Alt Başlığı", blank=True, null=True)

    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return self.site_name

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    icon = models.CharField(max_length=50, verbose_name="Kategori İkonu (ör: fas fa-code)", blank=True)

    class Meta:
        verbose_name = "Yetenek Kategorisi"
        verbose_name_plural = "Yetenek Kategorileri"

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills", verbose_name="Kategori")
    name = models.CharField(max_length=100, verbose_name="Yetenek Adı")
    image = models.ImageField(upload_to="skills/", verbose_name="Yetenek Görseli", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(verbose_name="Açıklama", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Skill.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']
        verbose_name = "Yetenek"
        verbose_name_plural = "Yetenekler"

    def __str__(self):
        return self.name
