from django.test import TestCase

# Create your tests here.
import string
import itertools
query = request.GET.get('q')
if not query.lower() in string.ascii_lowercase():
    ch1 = Post.objects.filter(title__contains=query.capitalise())
    ch2 = Post.objects.filter(title__contains=query)
    ch3 = Post.objects.filter(overview__contains=query.capitalise())
    ch4 = Post.objects.filter(overview__contains=query)
    que = result_list = list(itertools.chain(ch1, ch2, ch3, ch3))
    queryset = que.distinct()