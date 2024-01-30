from django.shortcuts import render

#import HttpResponse object from the django.http module
from django.http import HttpResponse

# Import the Category and Page models
from rango.models import Category
from rango.models import Page

from rango.forms import UserForm, UserProfileForm
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):

    #Query database for list of ALL categories stored.
    #Order by number of likes (descending).
    #Retrieve top 5, or all if less than 5.
    #Place list in context_dict dictionary (along with boldmessage)
    #that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]

    #Do the same for Pages
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage and categories matches to {{ boldmessage }} and {{ categoriess }} in the template!
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    context_dict = {'boldmessage': 'This tutorial has been put together by Juliana Cristina'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    #Create context dictionary which we can pass to the template rendering machine.
    context_dict = {}

    try:
        #Try to find a category name slug with given name.
        #if we can't, get() method raises a DoesNotExist exception
        #The get method ither returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all of the associated pages
        #filter() returns a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        #Add results list to template context under 'pages'.
        context_dict['pages'] = pages

        #We also add the category object from the database to context dictionary.
        #We use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        #Dont do anything - template will display "no category" message for us
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors, just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    #Describes to template if registration was successful.
    registered = False

    #If POST, we are processing data.
    if request.method == 'POST':
        #Grab information from raw form info.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #Save user's form data to database.
            user = user_form.save()

            #Hash password with the set_password method.
            #When hashed, update the user object.
            user.set_password(user.password)
            user.save()

            #Now we sort out the UserProfile instance.
            #We need to set the user attribute ourselves,
            #we set commit = false. This delays saving the model
            #until we are ready to avoid integrity problems.

            profile = profile_form.save(commit=False)
            profile.user = user

            #Did the user provide a profile picture?
            #If so, we need to get it from the input form and
            #put it in the UserProfile model.

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the UserProfile model instance.
            profile.save()

            #We update our variable to indictae that the template
            #registration was successful.

            registered = True
        else:
            #Invaid form or forms - mistakes or something else?
            #Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        #Not a HTTP POST, so render the form using two ModelForm instances.
        #These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
        # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
        
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
# The request is not a HTTP POST, so display the login form.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html')                      

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')  

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

