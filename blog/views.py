from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
# Create your views here.


def post_list(request):
    qs = Post.objects.all()
    qs  = qs.filter(published_date__lte=timezone.now())
    qs = qs.order_by('-published_date')
    return render(request, 'blog/post_list.html', {'post_list': qs})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})


def post_new(request):

    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user #비인증이면 튕김
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method =='POST':
        form = PostForm(request.POST, request.FILES, instance=post)#수정할 대상은 post다

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user #비인증이면 튕김
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.pk)
    else:
        form = PostForm(instance=post) #수정할 대상은 post다

    return render(request, 'blog/post_edit.html', {'form':form})
