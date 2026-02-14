from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render
# Notice the "view.py" is loaded once when you refresh but index() 
# is called whenever the page loads
print("view ran +++++++++++++++++++++++++++++++++++") 
def index(request):
    # This renders the 'base.html' template we created earlier
    #return HttpResponse("Hello, world, I'm iOS. I optimize inventories!")
    print("Print a log to the Django terminal, the cmd prompt where you started the app") # This goes to the terminal where you started Django

    # We will query the database here I think, and populate an item_dictionary and add it to the item_list
    # for each item in the DB
    item_dictionary = {}
    item_dictionary["name"] = "name1"
    item_dictionary["qty"] = "1"
    item_dictionary["uid"] = "123"
    page_data.append(item_dictionary)

    # display is the dictionary that is passed to the web page and all the
    # entries can be referenced in the HTML. See 'item_list' referenced in inventorysplash.html
    display = {
        "item_list" : page_data
    }    
    return render(request, 'inventorysplash.html', display)

def create_article(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Save the new model instance to the database
            form.save()
            return HttpResponse("Article created successfully!") # Redirect to a success page
    else:
        # If a GET (or any other method), create a blank form
        form = ArticleForm()
        
    return render(request, 'myapp/article_form.html', {'form': form})
