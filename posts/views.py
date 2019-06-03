from django.shortcuts import render
from posts.models import Post

def index(request):
    queryset = Post.objects.filter(featured=True).order_by('-timestamp')[0:13]
    row1 = queryset[0:3]
    row2 = queryset[3:6]
    row3_1 = queryset[6]
    row3_2 = queryset[7]
    row4 = queryset[8:11]
    row5_1 = queryset[11]
    row5_2 = queryset[12]
    context = {
        'row1' : row1,
        'row2' : row2,
        'row3_1' : row3_1,
        'row3_2' : row3_2,
        'row4' : row4,
        'row5_1' : row5_1,
        'row5_2' : row5_2
    }
    return render(request, 'index.html', context)

def single(request):
    return render(request, 'single.html', {})

def blog(request):
    return render(request, 'blog.html', {})

