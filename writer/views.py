from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . forms import ArticleForm, UpdateUserForm
from . models import Article
from account.models import CustomUser
from django.http import HttpResponseForbidden


# Create your views here.

@login_required(login_url='my-login')
def writer_dashboard(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    return render(request, 'writer/writer-dashboard.html')



@login_required(login_url='my-login')
def create_article(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('my-articles')
    context = {
        'CreateArticleForm': form,
    }
    return render(request, 'writer/create-article.html', context)



@login_required(login_url='my-login')
def my_articles(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    current_user = request.user.id
    article = Article.objects.all().filter(user=current_user)

    context = {
        'AllArticles':article,
    }
    return render(request, 'writer/my-articles.html', context)



@login_required(login_url='my-login')
def update_article(request, pk):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except:
        return redirect('my-articles')
    
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my-articles')
    context = {
        'UpdateArticleForm': form,
    }
    return render(request, 'writer/update-article.html', context)



@login_required(login_url='my-login')
def delete_article(request, pk):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except:
        return redirect('my-articles')
    
    if request.method == 'POST':
        article.delete()
        return redirect('my-articles')
    
    return render(request, 'writer/delete-article.html')



@login_required(login_url='my-login')
def account_management(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {
        'UpdateUserForm': form,
    }
    return render(request, 'writer/account-management.html', context)



@login_required(login_url='my-login')
def delete_account(request):
    if not request.user.is_writer:
        return HttpResponseForbidden("Clients cannot access this page.")
    
    if request.method == 'POST':
        deleteUser = CustomUser.objects.get(email=request.user)
        deleteUser.delete()
        return redirect('my-login')
    return render(request, 'writer/delete-account.html')




