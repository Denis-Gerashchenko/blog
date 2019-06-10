from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from posts.models import Post
from marketing.models import Signup

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

def single(request):
    recent = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'recent': recent,
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

# def recent(request):
#     queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:3]
#     context = {
#         'recent': queryset,
#     }
#     return render(request, 'footer.html', context)
