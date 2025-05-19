from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import BlogPost, Category, SubCategory, Education, Experience, Certificate, Project, Tag, CodeExample, About, SiteSettings, ContactInfo, Skill, SkillCategory, ProjectCategory, CodeLanguage, CodeCategory, NavbarLink

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    save_on_top = True
    date_hierarchy = 'created_at'

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "address")
    search_fields = ("full_name", "title", "address")

@admin.register(Education)
class EducationAdmin(BaseAdmin):
    list_display = ('title', 'school', 'date_range', 'is_current', 'gpa_display')
    list_filter = ('is_current', 'school', 'start_date')
    search_fields = ('title', 'school', 'description')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'school', 'description')
        }),
        ('Tarih Bilgileri', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Diğer Bilgiler', {
            'fields': ('gpa', 'tags')
        }),
    )

    def date_range(self, obj):
        if obj.is_current:
            return f"{obj.start_date.year} - Devam Ediyor"
        return f"{obj.start_date.year} - {obj.end_date.year}"
    date_range.short_description = "Tarih Aralığı"

    def gpa_display(self, obj):
        if obj.gpa:
            return f"{obj.gpa}/4.00"
        return "-"
    gpa_display.short_description = "GPA"

@admin.register(Experience)
class ExperienceAdmin(BaseAdmin):
    list_display = ('title', 'company', 'date_range', 'is_current')
    list_filter = ('is_current', 'company', 'start_date')
    search_fields = ('title', 'company', 'description')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'company', 'description')
        }),
        ('Tarih Bilgileri', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Etiketler', {
            'fields': ('tags',)
        }),
    )

    def date_range(self, obj):
        if obj.is_current:
            return f"{obj.start_date.year} - Devam Ediyor"
        return f"{obj.start_date.year} - {obj.end_date.year}"
    date_range.short_description = "Tarih Aralığı"

@admin.register(Certificate)
class CertificateAdmin(BaseAdmin):
    list_display = ('title', 'issuer', 'date', 'credential_id', 'slug', 'certificate_link')
    list_filter = ('issuer', 'date')
    search_fields = ('title', 'issuer', 'credential_id')
    prepopulated_fields = {'slug': ('title', 'issuer')}
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'issuer', 'date', 'description', 'order', 'slug')
        }),
        ('Sertifika Detayları', {
            'fields': ('credential_url', 'credential_id', 'image')
        }),
    )

    def certificate_link(self, obj):
        if obj.credential_url:
            return format_html('<a href="{}" target="_blank">Sertifikayı Görüntüle</a>', obj.credential_url)
        return "-"
    certificate_link.short_description = "Sertifika Linki"

@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('title', 'category', 'project_links', 'created_at', 'button_text', 'button_url')
    list_filter = ('category', 'created_at', 'tags')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Proje Detayları', {
            'fields': ('image', 'project_url', 'github_url', 'tags', 'button_text', 'button_url')
        }),
    )

    def project_links(self, obj):
        links = []
        if obj.project_url:
            links.append(f'<a href="{obj.project_url}" target="_blank">🌐</a>')
        if obj.github_url:
            links.append(f'<a href="{obj.github_url}" target="_blank">📦</a>')
        return format_html(' '.join(links)) if links else "-"
    project_links.short_description = "Proje Linkleri"

@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'slug', 'usage_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def usage_count(self, obj):
        count = (
            obj.education_tags.count() +
            obj.experience_tags.count() +
            obj.project_tags.count()
        )
        return count
    usage_count.short_description = "Kullanım Sayısı"

@admin.register(CodeExample)
class CodeExampleAdmin(BaseAdmin):
    list_display = ('title', 'language', 'category', 'created_at', 'preview_code')
    list_filter = ('language', 'category', 'created_at')
    search_fields = ('title', 'description', 'code')
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'language', 'category')
        }),
        ('Kod ve Açıklama', {
            'fields': ('code', 'description')
        }),
    )

    def preview_code(self, obj):
        return format_html('<pre><code>{}</code></pre>', obj.code[:100] + '...' if len(obj.code) > 100 else obj.code)
    preview_code.short_description = "Kod Önizleme"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "footer_text", "copyright")
    fieldsets = (
        ("Genel Bilgiler", {
            'fields': ("site_name", "logo", "cv_file")
        }),
        ("Footer Bilgileri", {
            'fields': ("footer_text", "copyright")
        }),
        ("Sosyal Medya", {
            'fields': ("github", "linkedin", "twitter", "instagram")
        }),
        ("İletişim Formu", {
            'fields': ("contact_title", "contact_subtitle", "contact_form_title", "contact_form_subtitle")
        }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "phone", "order")
    list_editable = ("order",)
    search_fields = ("title", "email", "phone", "address")
    list_filter = ("title",)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    ordering = ("category", "order")

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CodeLanguage)
class CodeLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CodeCategory)
class CodeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'section')
    ordering = ('order',)

# Admin Panel Özelleştirme
admin.site.site_header = "Murat YURDUGÜL - Yönetim Paneli"
admin.site.site_title = "Portfolio Yönetimi"
admin.site.index_title = "Hoş Geldiniz"
