from rest_framework import generics

from .models import Article
from .pagination import CustomArticlePagination
from .serializers import ArticleSerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(
            is_published=True
        ).order_by("created_at", "id")


class CustomArticleListView(ArticleListView):
    pagination_class = CustomArticlePagination