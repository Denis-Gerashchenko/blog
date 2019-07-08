class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:13]
        recent = Post.objects.order_by('-timestamp')[0:3]
        slides = Post.objects.filter(slide=True).order_by('timestamp')[0:4]

        context = {
                'row1': queryset[0:3],
                'row2': queryset[3:6],
                'row3_1': queryset[6],
                'row3_2': queryset[7],
                'row4': queryset[8:11],
                'row5_1': queryset[11],
                'row5_2': queryset[12],
                'recent': recent,
                'slides': slides,
        }
        return render(request, self.template_name, context)

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, UpdateView

from posts.models import Post, Author, PostViewCount, UserProfile, PostView
from .forms import CommentForm, PostForm
from marketing.models import Signup