import sys
sys.path.append("c:/Users/gaeta/Documents/SalesOps-1")
import dashboard.app as app

print("START OF HTML")
# Find the table body and print it
html = app.html if hasattr(app, 'html') else "NO HTML VAR"
# In app.py, html is a local variable in the tab section! Oh, we can't access it.
