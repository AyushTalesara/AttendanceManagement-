from __future__ import unicode_literals
from django.shortcuts import render,redirect,get_object_or_404 
from django.http import HttpResponse,Http404
from .forms import UserForm,studentregister,choices_1,teacherregister
from django.contrib.auth.forms import AuthenticationForm
import cv2,glob
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from faceRecog import dataset_fetch as df
from faceRecog import cascade as casc
from PIL import Image
from django.urls import reverse
from .models import student,teacher,subjects,attendances
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate, login,logout
from time import time
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pickle,os,datetime
from datetime import date
from faceRecog.settings import BASE_DIR
def register(request):
    form_class= UserForm
    template_name ='registration_form.html'

    if request.method=='GET' :
        form = form_class(None)
        return render(request,template_name,{'form': form})

    if request.method == 'POST' :
        form = form_class(request.POST)

        if form.is_valid():
            user  =form.save(commit=False)
            username= form.cleaned_data['username']
            password =form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # user = authenticate(username=username,password =password)
            # if user is not None:
            #     if user.is_active:
            #         login(request,user)
            #         return redirect('music:index')
            
        return redirect('test:fchoice')
def check(request):
    try:
        if request.user.is_authenticated:
            username12=request.user.username
            tripi=student.objects.filter(usn=username12)
            if tripi:
                return redirect('test:student-details',username12)
            else:
                return redirect('test:details-teacher',username12 ) 
        else:
            return redirect('test:login')  
    except:
        return redirect('test:logout')
def login_1(request):
    template_name='login.html'
    if request.method=="POST":
        form1 = AuthenticationForm(data=request.POST)
        if form1.is_valid():
            username= form1.cleaned_data['username']
            password =form1.cleaned_data['password']
            a=authenticate(username=username,password=password )
            if a is not None:
                login(request,a)
                teach=teacher.objects.filter(pid=username)
                tripi=student.objects.filter(usn=username)
                if tripi:
                    return redirect('test:student-details',username)
                elif teach:
                    return redirect('test:details-teacher',username )
                else:
                    raise Http404("This Username is not available")
    else:
        form1=AuthenticationForm(None)
    
    return render(request,template_name,{"form":form1})
def logout_1(request):
    logout(request)
    return redirect('/')
def enterdetails(request):
    form_class= studentregister
    template_name ='enterdetails.html'
    sub=subjects.objects.all()
    if request.method=='GET' :
        form = form_class(None)
        context={
            'form':form,
            'sub':sub
        }
        return render(request,template_name,context)
    if request.method == 'POST' :
        form = form_class(request.POST)
        if form.is_valid():
            user  =form.save(commit=False)
            user.save()
            subjectslist=request.POST.getlist('multip')
            for i in subjectslist:
                t=subjects.objects.get(subcode=i)
                t.usn.add(user)
                t.save()
                atten=attendances()
                atten.usn=user
                atten.subcode=t
                atten.save()
                
            userId=request.POST['usn']
            # print("hello")
            faceDetect = cv2.CascadeClassifier(BASE_DIR+'/static/ml/haarcascade_frontalface_default.xml')
            cam = cv2.VideoCapture(0)
            id = userId
            pathi=BASE_DIR+'/static/ml/dataset/user.'+str(id)
            lenght=len(glob.glob(pathi+'.*'))
            if lenght != 0:
                sampleNum =lenght
            else:
                sampleNum=0
            i=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                for(x,y,w,h) in faces:
                    sampleNum = sampleNum+1
                    i+=1
                    cv2.imwrite(BASE_DIR+'/static/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
                    cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
                    cv2.waitKey(250)
                cv2.imshow("Face",img)
                cv2.waitKey(1)
                if(i>25):
                    break
            cam.release()
            cv2.destroyAllWindows()
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            path = BASE_DIR+'/static/ml/dataset'
            cam = cv2.VideoCapture(0)
            def getImagesWithID(path):
                imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #concatinate the path with the image name
                faces = []
                Ids = []
                for imagePath in imagePaths:
                    faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
                    faceNp = np.array(faceImg, 'uint8')
                    ID = int(os.path.split(imagePath)[-1].split('.')[1]) 
                    faces.append(faceNp)
                    Ids.append(ID)
                    cv2.imshow("training", faceNp)
                    cv2.waitKey(10)
                return np.array(Ids), np.array(faces)
            ids, faces = getImagesWithID(path)
            recognizer.train(faces, ids)
            recognizer.save(BASE_DIR+'/static/ml/recognizer/trainingData.yml')
            cv2.destroyAllWindows()
            cam.release()
            return redirect('/')
    return render(request,template_name,context)


            
class StudentUpdate(UpdateView):
    model =student  
    fields=['usn','first_name','last_name','email']
    template_name_suffix = '_update_form'
class teacherUpdate(UpdateView):
    model =teacher
    fields=['pid','first_name','last_name']
    template_name_suffix = '_update_form'

# def details(request, id):
#     record = Records.objects.get(id=id)
#     context = {
#         'record' : record
#     }
#     return render(request, 'details.html', context)
f_date=date(2019,9,15)
now = datetime.datetime.now()
l_date=date(now.year,now.month,now.day)
dayst=np.busday_count(f_date,l_date)
#print("This is working ")
def teacherstudent(request):
    id=request.user.username 
    teacherid=teacher.objects.get(pid=id)
    subcode1=teacherid.subcode
    subje=subjects.objects.get(subcode =subcode1)
    list1=subje.usn.all()
    newlist=[]
    newlist2=[]
    for i in list1:
        attendances1=attendances.objects.get(usn=i.usn,subcode=subcode1)
        stu=student.objects.get(usn=i.usn)
        newlist2.append(stu.first_name+stu.last_name+'-'+str(i.usn))
        newlist.append(attendances1.attendance)
    mylist=zip(newlist2,newlist)
    context={
        'mylist':mylist,
        'differ':dayst

    }
    print("hello")
    return render(request,'teacherstudent.html',context)


def StudentDetails(request,id):
    
    student1 = get_object_or_404(student ,usn= id)
    attenda=attendances.objects.filter(usn=id)
    context={
        'student':student1,
        'attenda':attenda,
        'differ':dayst

    }
    return render(request,'detailstudent.html',context)
def DetailsTeacher(request,id):
    teacher1 = get_object_or_404(teacher ,pid= id)
    subje=teacher1.subjects_set.all()
    context={
        'teacher':teacher1,
        'subje':subje,
        'differ':dayst


    }
    return render(request,'detailsteacher.html',context) 
    

        
def teacherdetails(request):
    form_class= teacherregister
    template_name ='enterdetailsteacher.html'
    if request.method=='GET' :
        form = form_class(None)
        return render(request,template_name,{'form': form})
    if request.method == 'POST' :
        form = form_class(request.POST)
        if form.is_valid():
            user  =form.save(commit=False)
            user.save()
            user.subjects_set.create(subcode=form.cleaned_data['subcode'])
            userId=request.POST['pid']
            print (cv2.__version__)
            faceDetect = cv2.CascadeClassifier(BASE_DIR+'/static/ml/haarcascade_frontalface_default.xml')
            cam = cv2.VideoCapture(0)
            id = userId
            pathi=BASE_DIR+'/static/ml/dataset/user.'+str(id)
            lenght=len(glob.glob(pathi+'.*'))
            if lenght != 0:
                sampleNum =lenght
            else:
                sampleNum=0
            i=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                for(x,y,w,h) in faces:
                    sampleNum = sampleNum+1
                    i+=1
                    cv2.imwrite(BASE_DIR+'/static/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
                    cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
                    cv2.waitKey(250)
                cv2.imshow("Face",img)
                cv2.waitKey(1)
                if(i>25):
                    break
            cam.release()
            cv2.destroyAllWindows()
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            path = BASE_DIR+'/static/ml/dataset'
            cam = cv2.VideoCapture(0)
            def getImagesWithID(path):
                imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #concatinate the path with the image name
                faces = []
                Ids = []
                for imagePath in imagePaths:
                    faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
                    faceNp = np.array(faceImg, 'uint8')
                    ID = int(os.path.split(imagePath)[-1].split('.')[1]) 
                    faces.append(faceNp)
                    Ids.append(ID)
                    cv2.imshow("training", faceNp)
                    cv2.waitKey(10)
                return np.array(Ids), np.array(faces)
            ids, faces = getImagesWithID(path)
            recognizer.train(faces, ids)
            recognizer.save(BASE_DIR+'/static/ml/recognizer/trainingData.yml')
            cv2.destroyAllWindows()
            cam.release()
            return redirect('/')
    return render(request,template_name,{'form': form})
def fchoice(request):
    form1=choices_1(request.POST)
    if request.method == 'POST':
        if form1.is_valid():
            form4= form1.cleaned_data['display_type']
            if form4=='1':
                return redirect('test:enterdetails')
            else:
                return redirect('test:teacherdetails')
    return render(request, 'choices.html', {'form': form1})

def create_dataset(request,id):
    userId = id
    print (cv2.__version__)
    faceDetect = cv2.CascadeClassifier(BASE_DIR+'/static/ml/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    id = userId
    pathi=BASE_DIR+'/static/ml/dataset/user.'+str(id)
    lenght=len(glob.glob(pathi+'.*'))
    if lenght != 0:
        sampleNum =lenght
    else:
        sampleNum=0
    i=0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            sampleNum = sampleNum+1
            i+=1
            cv2.imwrite(BASE_DIR+'/static/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
            cv2.waitKey(250)
        cv2.imshow("Face",img)
        cv2.waitKey(1)
        if(i>25):
            break
    cam.release()
    cv2.destroyAllWindows()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = BASE_DIR+'/static/ml/dataset'
    cam = cv2.VideoCapture(0)

    def getImagesWithID(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #concatinate the path with the image name
        faces = []
        Ids = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1]) # -1 so that it will count from backwards and slipt the second index of the '.' Hence id
            faces.append(faceNp)
            # Label
            Ids.append(ID)
            #print ID
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(Ids), np.array(faces)
    ids, faces = getImagesWithID(path)
    recognizer.train(faces, ids)
    recognizer.save(BASE_DIR+'/static/ml/recognizer/trainingData.yml')
    cv2.destroyAllWindows()
    cam.release()
    tripi=student.objects.filter(usn=id)
    if tripi:
        return redirect('test:student-details',id)
    else:
        return redirect('test:details-teacher',id )
    