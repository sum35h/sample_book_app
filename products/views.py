from django.shortcuts import render
import requests
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect

class Books():
    def __init__(self,title,author,category,summary,image_url):
        self.title=title
        self.author=author
        self.category=category
        self.summary=summary
        self.image_url=image_url
        
    def __str__(self):
        return self.title+'-'+self.author

def search_books_api(query):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}'.format(query))
    
    items=json.loads(response.text)['items']
    
    result=[]
    
    for item in items:
        # print('#'*100)
      
        author_list=item.get('volumeInfo',{}).get('authors')
        
        authors=''
        if author_list != None:
            for i,author in enumerate(author_list):
                if i>0:
                    authors+=', '
                authors+=author
            
        category_list=item.get('volumeInfo',{}).get('categories')
        categories=''
        
        if category_list != None:
            for i,category in enumerate(category_list):
                if i>0:
                    categories+=', '
                categories+=category
                
        description=item.get('volumeInfo','No description').get('description','No description')
       
        description=description[:100]+'...'
            
        image_link=item.get('volumeInfo',{}).get('imageLinks',{}).get('smallThumbnail')
        
        title=item.get('volumeInfo',{}).get('title')
        # print(title,' ',authors,' ',categories)
        # print(image_link)
        # print(description)
        # print('#'*100)
        result.append(Books(title,authors,categories,description,image_link))
        
    return result
@csrf_exempt       
def home(request):
   
    if request.method == 'POST':

        query_string=request.POST['query_string']
        print(query_string,'-----------------')
        items=search_books_api(query_string)
        return render(request,'products/home.html',{'items':items,'home_active':'active'})
    else:  

        return render(request,'products/home.html',{'home_active':'active'})

   