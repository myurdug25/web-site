from django.urls import path
from . import views
from .views import project_detail, codeexample_detail, skill_detail

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('hakkimda/', views.about, name='about'),
    path('yetenekler/', views.skills, name='skills'),
    path('projeler/', views.projects, name='projects'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('projeler/<slug:slug>/', project_detail, name='project_detail'),
    path('kod/<slug:slug>/', codeexample_detail, name='codeexample_detail'),
    path('iletisim/', views.contact, name='contact'),
    path('yetenek/<slug:slug>/', skill_detail, name='skill_detail'),
    path('sertifika/<slug:slug>/', views.certificate_detail, name='certificate_detail'),
]
