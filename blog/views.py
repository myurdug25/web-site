from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import BlogPost, Category, SubCategory, Education, Experience, Certificate, Project, Tag, CodeExample, About, SiteSettings, ContactInfo, SkillCategory, Skill, ProjectCategory, CodeLanguage, CodeCategory

def home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    selected_subcategory = request.GET.get('subcategory')
    
    blog_yazilari = BlogPost.objects.all()
    
    if selected_category:
        blog_yazilari = blog_yazilari.filter(category__name=selected_category)
        if selected_subcategory:
            blog_yazilari = blog_yazilari.filter(subcategory__name=selected_subcategory)
    
    context = {
        'blog_yazilari': blog_yazilari.order_by('-tarih'),
        'categories': categories,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
    }
    
    return render(request, 'index.html', context)

def get_subcategories(request):
    category_name = request.GET.get('category')
    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            subcategories = list(category.subcategories.values('name'))
            return JsonResponse(subcategories, safe=False)
        except Category.DoesNotExist:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)

def detail(request, slug):
    yazi = BlogPost.objects.get(slug=slug)
    return render(request, 'detail.html', {'yazi': yazi})

def index(request):
    context = {
        'about': About.objects.first(),
        'educations': Education.objects.all(),
        'experiences': Experience.objects.all(),
        'certificates': Certificate.objects.all(),
        'projects': Project.objects.all(),
        'project_categories': ProjectCategory.objects.all(),
        'code_examples': CodeExample.objects.all(),
        'code_languages': CodeLanguage.objects.all(),
        'code_categories': CodeCategory.objects.all(),
        'tags': Tag.objects.all(),
        'site_settings': SiteSettings.objects.first(),
        'contact_infos': ContactInfo.objects.all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
    }
    return render(request, 'index.html', context)

def about(request):
    about = About.objects.first()
    context = {
        'about': about
    }
    return render(request, 'sections/about.html', context)

def skills(request):
    return render(request, 'sections/skills.html')

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'sections/projects.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Burada e-posta gönderme işlemi yapılabilir
        # Örnek: send_mail(subject, message, email, ['your@email.com'])
        
        return JsonResponse({
            'status': 'success',
            'message': 'Mesajınız başarıyla gönderildi.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Geçersiz istek.'
    }, status=400)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})

def codeexample_detail(request, slug):
    codeexample = get_object_or_404(CodeExample, slug=slug)
    return render(request, 'codeexample_detail.html', {'codeexample': codeexample})

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site_settings': settings}

def skill_detail(request, slug):
    skill = get_object_or_404(Skill, slug=slug)
    return render(request, 'skills/skill_detail.html', {'skill': skill, 'site_settings': SiteSettings.objects.first()})

def certificate_detail(request, slug):
    certificate = get_object_or_404(Certificate, slug=slug)
    return render(request, 'certificates/certificate_detail.html', {
        'certificate': certificate,
        'site_settings': SiteSettings.objects.first()
    })
