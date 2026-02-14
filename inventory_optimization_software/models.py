from django.db import models

# I think the database can be handled here and referenced in views. 
# When the view is refreshed just query the DB and build the item_list
# and the view will put it in the display
page_data = []
