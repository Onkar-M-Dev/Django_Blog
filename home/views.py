from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request): # HTML Page
    return render(request, 'home/home.html')
    #return HttpResponse("This is home")

def about(request): # HTML Page
    return render(request, 'home/about.html')
    #return HttpResponse("This is about")

def contact(request): # HTML Page
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly !")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent !")
    return render(request, 'home/contact.html')
    #return HttpResponse("This is contact")

def search(request): # HTML Page
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
    #allPosts = Post.objects.all()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)
    #return HttpResponse("This is search")

def handleSignup(request): # Authentication API
    if request.method == 'POST':
        # Get the POST parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should contain only letters and numbers")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCode Account has been successfully created !")
        return redirect('home')
    else:
        return HttpResponse('404-Not Found')
    
def handleLogin(request): # Authentication API
        if request.method == 'POST':
            loginusername = request.POST['loginusername']
            loginpass = request.POST['loginpass']

            user = authenticate(username=loginusername, password=loginpass)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in !")
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials, Please try again !")
                return redirect('home')

        return HttpResponse('404-Not Found')
    
def handleLogout(request): # Authentication API
        logout(request)
        messages.success(request,"Successfully logged out !")
        return redirect("home")
        