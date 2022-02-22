from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import *
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import  UserCreationForm
from  django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user
# Create your views here.
@unauthenticated_user
def registerPage(request):
  form = CreateUserForm()
  
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      # username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=user.username, password=raw_password)
      login(request, user)
      # group = Group.objects.get(name = "user")
      # user.groups.add(group)
      
      # messages.success(request,"Account created for" + username)
      return redirect('welcome')
  
  
  context = {'form':form}
  return render(request,'registration/register.html', context)


def welcome(request):
  return render(request,'welcome.html')

@unauthenticated_user
def loginPage(request):
  
  if request.method =='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse('user_profile', args=[username]))
    else:
      messages.info(request, "The user exists not")
      
  context = {}
  return render (request, 'registration/login.html', context)

def logoutUser(request):
  logout(request)
  return redirect('login')


# @unauthenticated_user
# @allowed_user(allowed_roles=['__all__'])
@login_required(login_url='login')
def index(request):
  profile = Profile.objects.get(user=request.user) 
  
  return render(request,'index.html',{'profile':profile})


@login_required(login_url='login')
# @allowed_user(allowed_roles=['user'])
  
def user_profile(request, username):
  user = get_object_or_404(User,username=username)  
  # new_user = request.user
  if request.method == 'POST':
    
    form = ProfileForm(request.POST, request.FILES)
    form_b = NeighbourhoodForm(request.POST)
    if form.is_valid() and form_b.is_valid():
      data = form_b.save()
      profile = form.save(commit=False)
      profile.user = request.user
      profile.neighbourhood = data
      profile.save()
      
      
      # profile = Profile.objects.get(user=user)
      
      return redirect('/')
  else:
    form = ProfileForm()
    form_b = NeighbourhoodForm()
      
  return render(request, 'new_profile.html',{'user':user,'form':ProfileForm, 'form_b':NeighbourhoodForm})   

@login_required(login_url='login')
# @allowed_user(allowed_roles=['user','admin'])
def hood_details(request,id):
  neighbourhood= get_object_or_404(Neighbourhood,pk=id)
  posts = Post.objects.filter(neighbourhood=neighbourhood)
  biz = Business.objects.filter(neighbourhood=neighbourhood)
  profile = Profile.objects.get(user=request.user)
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.neighbourhood = neighbourhood
      post.profile = profile
      post.save()
      
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      
    
  return render (request, 'neighbourhood_details.html',{'hood':neighbourhood,'form':PostForm,'posts':posts, 'biz':biz})
  
@login_required  
def profile(request,username):
  user = get_object_or_404(User,username=username)
  profile = Profile.objects.get(user=user)
  
  
  return render(request, 'profile.html',{'user':user,'profile':profile}) 

@login_required
def search_project(request):
  if 'business' in request.GET and request.GET["business"]:
    search_term = request.GET.get('business')
    searched_business = Business.search_business(search_term)
    message = f"{search_term}"
    
    return render (request, 'search.html',{"message":message, "business":searched_business})
  else:
    message = "Have you searched for any term?"
    return render (request,'search.html',{"message":message})
