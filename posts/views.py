from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post, Author, PostViewCount, UserProfile
from .forms import CommentForm, PostForm
from marketing.models import Signup


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

def search(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    recent = Post.objects.order_by('-timestamp')[0:3]
    if query:
        queryset = post_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
            ).distinct()
    context = {
        'queryset': queryset,
        'recent': recent,
    }
    return render(request, 'search_results.html', context)


def index(request):
    queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:13]
    recent = Post.objects.order_by('-timestamp')[0:3]

    context = {
        'row1' : queryset[0:3],
        'row2' : queryset[3:6],
        'row3_1' : queryset[6],
        'row3_2' : queryset[7],
        'row4' : queryset[8:11],
        'row5_1' : queryset[11],
        'row5_2' : queryset[12],
        'recent': recent,
    }
    return render(request, 'index.html', context)


def single(request, id):
    recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)

    #Pagination logic
    previous_p = None
    next_p = None
    key = int(id)
    #a queryset of posts with id anotated like this: <QuerySet [{'id': 1}, {'id': 2}, etc
    query = Post.objects.order_by('timestamp').values('id').annotate()
    listed_query = list(query)
    #a position of a post in a whole timeline for pagination
    index_of_post = [listed_query.index(post) for post in listed_query if post['id'] == key][0]
    try:
        previous_post_id = listed_query[index_of_post - 1]['id']
    except IndexError:
        previous_p = False
    try:
        next_post_id = listed_query[index_of_post + 1]['id']
    except IndexError:
        next_p = False
    previous_p = get_object_or_404(Post, id=previous_post_id) if not previous_p is False else False
    next_p = get_object_or_404(Post, id=next_post_id) if not next_p is False else False
    #end of pagination logic

    if request.user.is_authenticated:
        PostViewCount.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': post.id
            }))

    if request.method == 'POST':
        email = request.POST.get('email', False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'post': post,
        'previous': previous_p,
        'next': next_p,
        'form': form,
        'recent': recent,
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
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    recent = Post.objects.order_by('-timestamp')[0:3]
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


def blog(request):
    queryset = Post.objects.order_by('-timestamp')
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

    if request.method == 'POST':
        email = request.POST.get('email', False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'row1': paginated_queryset[0:2],
        'row2': paginated_queryset[2:4],
        'row3': paginated_queryset[4:6],
        'row4': paginated_queryset[6:8],
        'row5': paginated_queryset[8:10],
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'recent': recent,
    }
    return render(request, 'blog.html', context)


def test(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'recent': recent,
    }
    return render(request, 'test.html', context)


def profile(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    prof = get_user_profile(request.user)
    form = UserProfile(request.POST or None, request.FILES or None)
    if not prof:
        form.user_id = request.user.id
        form.save()
    context = {
        'recent': recent,
    }
    return render(request, 'profile.html', context)


