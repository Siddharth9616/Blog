from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# HTML Pages
def home(request):
    allPosts= Post.objects.all().order_by('-timeStamp')[:4]
    context = {'allPosts': allPosts}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        content= request.POST['content']
        
        # if len(name)<2 or len(email)<3 or len(phone)<5 or len(content)<3:
        #     messages.error(request, "Please fill the form correctly")
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        return redirect('contact_success')
    return render(request, 'home/contact.html')

def contact_success(request):
    return render(request, 'home/contact_success.html')

def search(request):
    queary = request.GET.get('queary')
    if len(queary)>70:
        allPosts= []
    else:
        allPoststitle = Post.objects.filter(title__icontains= queary)
        allPostsContent = Post.objects.filter(content__icontains= queary)
        allPosts = allPoststitle.union(allPostsContent)

    params = {'allPosts': allPosts, 'queary':queary}
    return render(request, 'home/search.html', params)


# Authentication s
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #Check for errorneous input
        # username should be under 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('home')
        
         # Optional: check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('home')
        
        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match ")
            return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, "Signup successful! Welcome, " + username + "!")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")
    
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
        

    return HttpResponse('404 - Not Found')
       
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


    