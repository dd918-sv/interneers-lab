from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.http import JsonResponse

def hello_world(request):
    name=request.GET.get("name","World")
    return JsonResponse({"message":f"Hello,{name}!"})

def bmi(request):
    name=request.GET.get("name")
    height=request.GET.get("height_in_ft")
    weight=request.GET.get("weight_in_kg")
    if name==None:
        return JsonResponse({"error":"Please provide a name"},status=400)
    if height==None:
        return JsonResponse({"error":f"Hi {name}.Please provide a height"},status=400)
    if weight==None:
        return JsonResponse({"error":f"Hi {name}.Please provide a weight"},status=400)
    
    if height[-2:]!="ft":
        return JsonResponse({"error":f"{height[-2:0]} Hi {name}.Please provide height in ft with ft as suffix after actual value"},status=400)
    if weight[-2:]!='kg':
        return JsonResponse({"error":f"Hi {name}.Please provide weight in kg with kg as suffix after actual value"},status=400)
    
    height=height[0:-2]
    weight=weight[0:-2]
    for h in height:
        if h.isnumeric()==False and h!='.':
            return JsonResponse({"error":"Bruh! How come height's numeric value contain a non-numeric character in between!!"},status=400)
    for w in weight:
        if w.isnumeric()==False:
            return JsonResponse({"error":"Bruh! How come weight's numeric value contain a non-numeric character in between!!"},status=400)
    try:
        height=float(height)
    except:
        return JsonResponse({"error":"Please provide a valid height"},status=400)
    try:
        weight=float(weight)
    except:
        return JsonResponse({"error":"Please provide a valid weight"},status=400)

    height=height*0.3048
    bmi=weight/(height*height)
    bmi=round(bmi,2)

    if bmi<18.5:
        return JsonResponse({"message":f"Hello,{name}! Your BMI is {bmi}. You are underweight. Excercise and eat healthy."})
    elif bmi>=18.5 and bmi<24.9:
        return JsonResponse({"message":f"Hello,{name}! Your BMI is {bmi}. You are healthy."})
    else:
        return JsonResponse({"message":f"Hello,{name}! Your BMI is {bmi}.You are overweight. Excercise and eat healthy."})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('bmi/', bmi),
]
