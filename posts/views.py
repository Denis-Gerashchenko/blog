from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post
from .forms import CommentForm
from marketing.models import Signup


def search(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = post_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
            ).distinct()
    context = {
        'queryset': queryset,
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
    query = Post.objects.values('id').annotate()
    list_of_id = [a_dict['id'] for a_dict in query]

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': post.id
            }))
    if post.id != min(list_of_id):
        previous_p = get_object_or_404(Post, id=str(int(id)-1))
    else:
        previous_p = False
    if post.id != max(list_of_id):
        next_p = get_object_or_404(Post, id=str(int(id) + 1))
    else:
        next_p = False

    if request.method == 'POST':
        email = request.POST.get('email', False)
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'recent': recent,
        'post': post,
        'previous': previous_p,
        'next': next_p,
        'form': form,
    }
    return render(request, 'single.html', context)


def blog(request):
    queryset = Post.objects.all()
    paginator = Paginator(queryset, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    recent = Post.objects.order_by('-timestamp')[0:3]

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
        'recent': recent,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
    }
    return render(request, 'blog.html', context)

def test(request):
    return render(request, 'test.html', {})