from django.urls import path

from .views import ArticleListView, CustomArticleListView


urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path(
        "articles/custom/",
        CustomArticleListView.as_view(),
        name="custom-article-list",
    ),
]