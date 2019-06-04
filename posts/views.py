from django.shortcuts import render
from posts.models import Post

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
    queryset = Post.objects.order_by('-timestamp')[0:10]
    recent = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'row1': queryset[0:2],
        'row2': queryset[2:4],
        'row3': queryset[4:6],
        'row4': queryset[6:8],
        'row5': queryset[8:10],
        'recent': recent,
        'queryset': queryset,
    }
    return render(request, 'blog.html', context)

# def recent(request):
#     queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:3]
#     context = {
#         'recent': queryset,
#     }
#     return render(request, 'footer.html', context)
