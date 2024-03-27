from django.urls import path
from .views import(news_list, list_detail, HomePageView, ContactPageView, page404,
                   LocalNewsView, TechnologyNewsView, SportNewsView, ForeignNewsView)

urlpatterns = [
    path("news/", news_list, name="all_news_list"),
    path("detail/<slug:news>/", list_detail, name="news_detail_page"),
    path("", HomePageView.as_view(), name='home_page'),
    path("contact-us/", ContactPageView.as_view(), name="contact_page"),
    path("404_page", page404, name='404_page'),
    path('local-news/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/news/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
]