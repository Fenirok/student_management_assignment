from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GlobalArticlePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50


class CustomArticlePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_page_size(self, request):
        raw_value = request.query_params.get(self.page_size_query_param)

        if raw_value is None:
            return self.page_size

        try:
            page_size = int(raw_value)
        except (TypeError, ValueError):
            raise ValidationError({
                "page_size": "Enter a whole number greater than 0."
            })

        if page_size <= 0:
            raise ValidationError({
                "page_size": "Enter a whole number greater than 0."
            })

        if page_size > self.max_page_size:
            raise ValidationError({
                "page_size": f"Ensure this value is no greater than {self.max_page_size}."
            })

        return page_size

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "page_info": {
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
            },
            "items_info": {
                "page_size": self.get_page_size(self.request),
                "returned": len(data),
                "total": self.page.paginator.count,
            },
            "results": data,
        })