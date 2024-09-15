from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    """
    View to list all blog posts.
    """
    posts = Post.objects.all()  # Retrieve all posts from the database
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """
    View to display a single blog post by its ID.
    """
    post = get_object_or_404(Post, pk=pk)  # Retrieve the post with the given ID, or return a 404 if not found
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    """
    View to create a new blog post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the current user
            post.save()  # Save the form data to the database
            return redirect('post_list')  # Redirect to the list of blog posts after saving
    else:
        form = PostForm()  # Display an empty form for GET requests

    return render(request, 'blog/post_create.html', {'form': form})  # Render the form template

def post_edit(request, pk):
    """
    View to edit a blog post.
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author of the post
    if request.user != post.author:
        return redirect('post_detail', pk=pk)  # Redirect to the post detail page if not authorized

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    """
    View to delete a blog post.
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user is the author of the post
    if request.user != post.author:
        return redirect('post_detail', pk=pk)  # Redirect to the post detail page if not authorized

    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user immediately after registration
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})