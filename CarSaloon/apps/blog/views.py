from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage 
from django.conf import settings
from .forms import *
from .models import *
#  Create your views here.

def index(request):
    blogs=Blog.objects.all()
    context={
        "blogs":blogs,
        'media_url':settings.MEDIA_URL,     #DOest work , should fix it , Photoes dont come on Form 
    } 
    return render(request,"blog/index.html",context)

def XXXXXXXXXX(request):
    if request.method=="POST":
        form=BlogForm(request.POST) #==>request.FILES  is  Dictionary of  all file:
        if form.is_valid():
           data=form.cleaned_data
           blog=Blog() # from our model we create a instance
           blog.title=data['title']
           blog.description=data['description'] 
           blog.is_active=data['is_active']
           blog.save()
           return redirect(request,"blog/index.html")
           #return render(request,"blog/index.html") 
         
    else:
        form=BlogForm()
        context={
            'form': form, 
          
        }  
    return render(request, "blog/create.html",context)
             
    

#======================================================================================================
def create_blog(request):
    if request.method=="POST":
        form=BlogForm(request.POST,request.FILES) #==>request.FILES  is  Dictionary of  all file:
        if form.is_valid():
            imageUpload=request.FILES['main_img']
            if imageUpload.size<1000000:
                if imageUpload.content_type=="image/jpeg" or imageUpload.content_type=="image/png":
                # if imageUpload.count_type=="image/jpeg" or imageUpload.count_type=="image/png" : 
                        #To avoid (dublicate Names or   changes in db with our Project )the Same Names we  Generate our name Prefix or suffix added to the Name:
                        import os 
                        import datetime
                        imgName,ext=os.path.splitext(imageUpload.name)
                        currenttime=datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
                    
                        # imagePath='images/blogimg/'+imageUpload.name
                        imagePath='images/blogimg/'+imgName+currenttime+ext
                       
                        #storage of data on the db:       blog=Blog (our model):    cleaned form=>(data)=form=BlogForm
                        data=form.cleaned_data
                        blog=Blog() # from our model we create a instance
                        blog.title=data['title']
                        blog.description= data['description']
                        blog.is_active=data['is_active']
                        blog.save()
                         #storage of data on Server
                        fss=FileSystemStorage()
                        # fss.save('images/blogimg/'+imageUpload.name, imageUpload)
                        fss.save(imagePath, imageUpload)
                        return render(request,"blog/index.html")
                    
                     
                else:
                    context={ 'form':form,
                        'message':'Type OF File not GOOD'
                    }
                  
        
            else:
                context={
                    'form':form,
                    'message':'Size is bigger than 10 kilo byte'
                }
             
        
 
    else:
        form=BlogForm()
        context={
            'form':form,
        }
    return render(request,"blog/create.html",context)






















