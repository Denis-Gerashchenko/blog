from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, UpdateView

from posts.models import Post, Author, PostViewCount, UserProfile, PostView, User, Comment, Category
from .forms import CommentForm, PostForm, ProfileForm
from marketing.models import Signup

import string
import itertools


def get_category(title):
    cat = Category.objects.filter(title=title)
    return cat[0].id


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_user_profile(user):
    qs = UserProfile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_user_id(username):
    qs = User.objects.filter(username=username)
    if qs.exists():
        return qs[0].id
    return None


def search(request):
    post_list = Post.objects.all()
    recent = Post.objects.order_by('-timestamp')[0:3]
    query = request.GET.get('q')
    if query:
        queryset = post_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'recent': recent,
        'query': query,
    }
    return render(request, 'search_results.html', context)


def categories(request, title):
    name = title
    recent = Post.objects.order_by('-timestamp')[0:3]
    queryset = Post.objects.filter(category_id=get_category(title))
    context = {
        'queryset': queryset,
        'recent': recent,
        'name': name,
    }
    return render(request, 'category-results.html', context)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:13]
        recent = Post.objects.order_by('-timestamp')[0:3]
        slides = Post.objects.filter(slide=True).order_by('timestamp')[0:4]

        if queryset:
            context = {
                    'queryset': queryset,
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
        else:
            context = {}
        return render(request, self.template_name, context)


def single(request, id):
    recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.all()

    # Next-previous post logic
    previous_p = None
    next_p = None
    key = int(id)
    # a queryset of posts with id annotated like this: <QuerySet [{'id': 1}, {'id': 2}, etc
    query = Post.objects.order_by('timestamp').values('id').annotate()
    listed_query = list(query)
    # a position of a post in a whole timeline for pagination
    index_of_post = [listed_query.index(post) for post in listed_query if post['id'] == key][0]
    # try:
    #     previous_post_id = listed_query[index_of_post - 1]['id']
    # except IndexError:
    #     previous_p = False
    if not index_of_post == 0:
        previous_post_id = listed_query[index_of_post - 1]['id']
    else:
        previous_p = False
    try:
        next_post_id = listed_query[index_of_post + 1]['id']
    except IndexError:
        next_p = False
    previous_p = get_object_or_404(Post, id=previous_post_id) if not previous_p is False else False
    next_p = get_object_or_404(Post, id=next_post_id) if not next_p is False else False
    # end of next-previous post logic

    if request.user.is_authenticated:
        PostViewCount.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            form.instance.user = request.user
            form.instance.post = post
            form.instance.reply = comment_qs
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': post.id
            }))

    if request.method == 'POST':
        email = request.POST.get('email', False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    # if request.method == 'POST':
    #     k = request.POST.get('parent_id', False)
    #     print(k)

    context = {
        'post': post,
        'previous': previous_p,
        'next': next_p,
        'form': form,
        'recent': recent,
        'categories': categories,
    }
    return render(request, 'single.html', context)


def update(request, id):
    recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)
    updt = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=post)

    author = get_author(request.user)

    if request.method == 'POST':
        if updt.is_valid():
            updt.instance.author = author
            updt.save()
            return redirect(reverse('post-detail', kwargs={
                'id': updt.instance.id
            }))
    context = {
        'updt': updt,
        'recent': recent,
    }
    return render(request, 'post-update.html', context)


def create(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))

    context = {
        'form': form,
        'recent': recent,
    }
    return render(request, 'post-create.html', context)


def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post-list'))


def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect(reverse('post-detail', kwargs={
                'id': comment.post.id}))


class BlogView(View):
    template_name = 'blog.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        queryset = Post.objects.order_by('-timestamp')
        if queryset:
            paginator = Paginator(queryset, 10)
            page_request_var = 'page'
            page = request.GET.get(page_request_var)
            recent = Post.objects.order_by('-timestamp')[0:3]
            try:
                paginated_queryset = paginator.page(page)
            except PageNotAnInteger:
                paginated_queryset = paginator.page(1)
            except EmptyPage:
                paginated_queryset = paginator.page(paginator.num_pages)
            a = paginated_queryset.has_other_pages
            context = {
                'row1': paginated_queryset[0:2],
                'row2': paginated_queryset[2:4],
                'row3': paginated_queryset[4:6],
                'row4': paginated_queryset[6:8],
                'row5': paginated_queryset[8:10],
                'queryset': paginated_queryset,
                'page_request_var': page_request_var,
                'recent': recent,
                'categories': categories,
                'a': a,
            }
        else:
            context = {}
        return render(request, 'blog.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        return redirect('post-list')


def profile(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    prof = get_user_profile(request.user)
    form = UserProfile(request.POST or None, request.FILES or None)
    if not prof:
        form.user_id = request.user.id
        form.profile_picture = 'human.png'
        form.save()
        prof = get_user_profile(request.user)
    context = {
        'recent': recent,
        'profile': prof,
    }
    return render(request, 'profile.html', context)


class UpdateProfileView(UpdateView):
    template_name = 'profile-update.html'
    model = UserProfile
    form_class = ProfileForm

    def get_object(self):
        prof = get_user_profile(self.request.user)
        return prof

    def get_context_data(self, **kwargs):
        recent = Post.objects.order_by('-timestamp')[0:3]
        context = super().get_context_data(**kwargs)
        context['recent'] = recent
        return context

    def form_valid(self, form):
        form.user_id = self.request.user.id
        form.save()
        return redirect(reverse('profile'))


def another_user_view(request, username):
    if request.user.username == username:
        return redirect(reverse('profile'))
    recent = Post.objects.order_by('-timestamp')[0:3]
    user = get_object_or_404(UserProfile, user_id=get_user_id(username))

    context = {
        'recent': recent,
        'person': user,
    }
    return render(request, 'another-user.html', context)


def contact_view(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'recent': recent,
    }
    return render(request, 'contact.html', context)

