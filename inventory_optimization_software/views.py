from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render
# Notice the "view.py" is loaded once when you refresh but index() 
# is called whenever the page loads
print("view ran +++++++++++++++++++++++++++++++++++") 


def index(request):
    if request.method == "POST":
        if request.POST.get("clear_button") == "clear_button":
            page_data.clear()
        username = request.POST.get("itemname")
        if username:
            # We will query the database in models.py, and populate an item_dictionary and add it to the item_list
            # for each item in the DB or something
            item_dictionary = {}
            item_dictionary["name"] = username
            item_dictionary["qty"] = request.POST.get("itemquantity")
            item_dictionary["uid"] = 123
            page_data.append(item_dictionary)            
        else:
            print("OR ELSE")

        
    # This renders the 'base.html' template we created earlier
    #return HttpResponse("Hello, world, I'm iOS. I optimize inventories!")
    print("Print a log to the Django terminal, the cmd prompt where you started the app") # This goes to the terminal where you started Django



    # display is the dictionary that is passed to the web page and all the
    # entries can be referenced in the HTML. See 'item_list' referenced in inventorysplash.html
    display = {
        "item_list" : page_data
    }    
    return render(request, 'inventorysplash.html', display)


# def create_article(request):
#     if request.method == 'POST':
#         # Create a form instance and populate it with data from the request
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             # Save the new model instance to the database
#             form.save()
#             return HttpResponse("Article created successfully!") # Redirect to a success page
#     else:
#         # If a GET (or any other method), create a blank form
#         form = ArticleForm()
        
#     return render(request, 'myapp/article_form.html', {'form': form})
