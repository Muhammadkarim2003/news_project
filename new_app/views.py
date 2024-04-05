from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .custom_permission import OnlyLoggedSuperuser, UserPassesTestMixin
from hitcount.models import HitCount
from hitcount.views import HitCountDetailView, HitCountMixin
from hitcount.utils import get_hitcount_model








# Create your views here.
def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


# @login_required
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits



    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    news_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    contex = {
        "news": news,
        'comments': comments,
        'new_comment': news_comment,
        'comment_form': comment_form,
        'comment_count': comment_count
    }
    return render(request, 'news/news_detail.html', contex)



class HomePageView(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categorys'] = Category.objects.all()
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:4]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name='Mahalliy').order_by("publish_time")[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name='Xorij').order_by("publish_time")[:6]
        context['sport_xabarlar'] = News.published.all().filter(category__name='Sport').order_by("publish_time")[:6]
        context['texnologiya_xabarlar'] = News.published.all().filter(category__name='Texnologiya').order_by("publish_time")[:6]


        return context




class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langaniz uchun rahmat!</1>")


def page404(request):
    context = {

    }
    return render(request, 'news/404.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news



class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class NewsUpdateView(OnlyLoggedSuperuser, UpdateView):
    model = News
    fields = ['title', 'body', 'images', 'category', 'status']
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperuser, DetailView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreadeView(OnlyLoggedSuperuser, CreateView):
    model = News
    template_name = 'crud/news_creat.html'
    fields = ['title', 'slug', 'body', 'images', 'category', 'status']
@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )



















# def HomePageView(request):
#     news_list = News.published.all().order_by('-publish_time')[:15]
#     local_one = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name='Mahalliy')[1:6]
#     categorys = Category.objects.all()
#     context = {
#         "news_list": news_list,
#         "categorys": categorys,
#         "local_one": local_one,
#         "local_news": local_news,
#     }
#     return render(request, 'news/index.html', context)








# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaniz uchun rahmat</h2>")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)