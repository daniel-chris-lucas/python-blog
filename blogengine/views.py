from blogengine.models import Category, Post
from django.shortcuts import render
from django.views.generic import ListView


class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        try:
            category = Category.objects.get(slug=slug)
            return Post.objects.filter(category=category)
        except Category.DoesNotExist:
            return Post.objects.none()
