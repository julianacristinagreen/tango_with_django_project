from django.shortcuts import render

#import HttpResponse object from the django.http module
from django.http import HttpResponse

# Import the Category and Page models
from rango.models import Category
from rango.models import Page

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
