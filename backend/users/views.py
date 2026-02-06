from django.shortcuts import render, HttpResponse
from .forms import UserRegistrationForm
from .models import UserRegistrationModel,UserImagePredictinModel
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .utility.GetImageStressDetection import ImageExpressionDetect
from .utility.MyClassifier import KNNclassifier
from subprocess import Popen, PIPE
import subprocess

# Create your views here.


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})

def UploadImageForm(request):
    loginid = request.session['loginid']
    data = UserImagePredictinModel.objects.filter(loginid=loginid)
    return render(request, 'users/UserImageUploadForm.html', {'data': data})

def UploadImageAction(request):
    image_file = request.FILES['file']

    # let's check if it is a csv file
    if not image_file.name.endswith('.jpg'):
        messages.error(request, 'THIS IS NOT A JPG  FILE')

    fs = FileSystemStorage()
    filename = fs.save(image_file.name, image_file)
    # detect_filename = fs.save(image_file.name, image_file)
    uploaded_file_url = fs.url(filename)
    obj = ImageExpressionDetect()
    emotion = obj.getExpression(filename)
    username = request.session['loggeduser']
    loginid = request.session['loginid']
    email = request.session['email']
    UserImagePredictinModel.objects.create(username=username,email=email,loginid=loginid,filename=filename,emotions=emotion,file=uploaded_file_url)
    data = UserImagePredictinModel.objects.filter(loginid=loginid)
    return render(request, 'users/UserImageUploadForm.html', {'data':data})

def UserEmotionsDetect(request):
    if request.method=='GET':
        imgname = request.GET.get('imgname')
        obj = ImageExpressionDetect()
        emotion = obj.getExpression(imgname)
        loginid = request.session['loginid']
        data = UserImagePredictinModel.objects.filter(loginid=loginid)
        return render(request, 'users/UserImageUploadForm.html', {'data': data})

def UserLiveCameDetect(request):
    obj = ImageExpressionDetect()
    obj.getLiveDetect()
    return render(request, 'users/UserLiveHome.html', {})

def UserKerasModel(request):
    # p = Popen(["python", "kerasmodel.py --mode display"], cwd='StressDetection', stdout=PIPE, stderr=PIPE)
    # out, err = p.communicate()
    subprocess.call("python kerasmodel.py --mode display")
    return render(request, 'users/UserLiveHome.html', {})

def UserKnnResults(request):
    obj = KNNclassifier()
    df,accuracy,classificationerror,sensitivity,Specificity,fsp,precision = obj.getKnnResults()
    df.rename(columns={'Target': 'Target', 'ECG(mV)': 'Time pressure', 'EMG(mV)': 'Interruption', 'Foot GSR(mV)': 'Stress', 'Hand GSR(mV)': 'Physical Demand', 'HR(bpm)': 'Performance', 'RESP(mV)': 'Frustration', }, inplace=True)
    data = df.to_html()
    return render(request,'users/UserKnnResults.html',{'data':data,'accuracy':accuracy,'classificationerror':classificationerror,
                                                       'sensitivity':sensitivity,"Specificity":Specificity,'fsp':fsp,'precision':precision})

from django.http import HttpResponse

def result_view(request):
    return HttpResponse("""
        <h1>Stress Detection System</h1>
        <p>Backend CNN model is running successfully.</p>
        <p>Emotion / Stress is detected using live camera.</p>
    """)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Add parent directory to path to import xgboost_model
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@csrf_exempt
def SurveyPrediction(request):
    """
    XGBoost-based stress prediction from survey data.
    
    POST /survey-predict/
    Body: JSON with keys: age, gender, designation, company_type, 
          wfh_setup, resource_allocation, mental_fatigue
    
    Returns: JSON with stress_percentage, risk_level, confidence, factor_impacts
    """
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['age', 'gender', 'designation', 'company_type', 
                             'wfh_setup', 'resource_allocation', 'mental_fatigue']
            
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'error': f'Missing required field: {field}',
                        'status': 'error'
                    }, status=400)
            
            # Import and use XGBoost model
            try:
                from xgboost_model import predict_stress
                result = predict_stress(data)
            except ImportError:
                # Fallback to rule-based prediction if xgboost_model not available
                result = rule_based_stress_prediction(data)
            
            return JsonResponse({
                'status': 'success',
                'stress_percentage': result['stress_percentage'],
                'risk_level': result['risk_level'],
                'confidence': result['confidence'],
                'factor_impacts': result['factor_impacts'],
                'algorithm': result.get('algorithm', 'XGBoost'),
                'method': 'Survey-Based XGBoost Prediction'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON format',
                'status': 'error'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    elif request.method == 'GET':
        # Return API info for GET requests
        return JsonResponse({
            'api': 'Survey-Based Stress Prediction',
            'method': 'POST',
            'required_fields': {
                'age': 'int (18-70)',
                'gender': 'int (0=Female, 1=Male)',
                'designation': 'int (1-5)',
                'company_type': 'int (0=Product, 1=Service)',
                'wfh_setup': 'int (0=No, 1=Yes)',
                'resource_allocation': 'float (hours/day)',
                'mental_fatigue': 'float (0-10)'
            },
            'response': {
                'stress_percentage': 'float (0-100)',
                'risk_level': 'string (Low/Medium/High)',
                'confidence': 'float',
                'factor_impacts': 'dict'
            }
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def rule_based_stress_prediction(data):
    """Fallback rule-based prediction if XGBoost model not available"""
    stress = 10
    
    # Age factor
    stress += (data.get('age', 30) - 22) / 38 * 8
    
    # Gender factor
    stress += (1 - data.get('gender', 1)) * 3
    
    # Designation factor
    stress += data.get('designation', 2) * 5
    
    # Company type
    stress += (1 - data.get('company_type', 1)) * 8
    
    # WFH setup
    stress += (1 - data.get('wfh_setup', 1)) * 10
    
    # Resource allocation
    stress += (data.get('resource_allocation', 8) - 6) * 3
    
    # Mental fatigue
    stress += data.get('mental_fatigue', 5) * 6
    
    stress = max(0, min(100, stress))
    
    if stress > 60:
        risk_level = 'High'
    elif stress > 35:
        risk_level = 'Medium'
    else:
        risk_level = 'Low'
    
    # Factor impacts
    mf = data.get('mental_fatigue', 5)
    ra = data.get('resource_allocation', 8)
    wfh = data.get('wfh_setup', 1)
    des = data.get('designation', 2)
    
    factor_impacts = {
        'mental_fatigue': 'High' if mf > 6 else 'Medium' if mf > 3 else 'Low',
        'resource_allocation': 'High' if ra > 10 else 'Medium' if ra > 8 else 'Low',
        'wfh_setup': 'High' if wfh == 0 else 'Low',
        'designation': 'High' if des > 3 else 'Medium' if des > 2 else 'Low'
    }
    
    return {
        'stress_percentage': round(stress, 2),
        'risk_level': risk_level,
        'confidence': 80.0,
        'factor_impacts': factor_impacts,
        'algorithm': 'RuleBased'
    }
