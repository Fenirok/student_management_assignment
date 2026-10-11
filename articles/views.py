from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 10


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        return Article.objects.filter(
            is_published=True
        ).order_by("created_at", "id")

