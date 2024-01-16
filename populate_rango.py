#Lines 2-7 important for importing modules.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    #Create list of dictionaries contraining the pages we want to add in each category
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
         'url':'http://flask.pocoo.org'}
    ]

    #dictionary of dictionaries for the categories
    cats = {
        'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
         'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
         'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
        }
    
    #Code below goes through cats dictionary, then adds each category,
    #then adds all the associated pages for that category.

    #Loop iterates over items (key-value pairs) in the 'cats' dictionary. Each iteration represents 
    #a category of cats ('cat') and its associated data ('cat_data).
    for cat, cat_data in cats.items():
        #Creates new 'Category' object with the name 'cat' and stores new object in 'c'
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        #Iterates through the associated 'pages' data in the current 'Category' object.
        for p in cat_data['pages']:
            #Creates new 'Page' object with the associated category, page title, and url.
            add_page(c, p['title'], p['url'])

    #Prints out the categories we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f' - {c}: {p}')

def add_page(cat,title,url,views=0):  
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p
    
def add_cat(name,views=0,likes=0):
    #Find the object with given 'name' parameter. If it is not found, create new 'Category' object.If found, returns the object.
    #The [0] ensures that functions always returns the actual object.
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
    
#Execution starts here

#Code within the conditional statement below will only be executed when ran as standalone Python script.
#Importnig the module will not run this code, any classes or functionals will be fully accessable however.
if __name__ == '__main__':
    print('Starting Rango population script...')
    #Keeps tabs on categories that are created.
    populate()
