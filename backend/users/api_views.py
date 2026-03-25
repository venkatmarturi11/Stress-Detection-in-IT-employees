from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import UserRegistrationModel, UserImagePredictionModel, UserSurveyPredictionModel
import json
import datetime

@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email', '').lower()
            mobile = data.get('mobile')
            password = data.get('password')
            
            if not all([name, email, password]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
            if UserRegistrationModel.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already registered'}, status=400)
            
            user = UserRegistrationModel.objects.create(
                name=name,
                email=email,
                loginid=email, # Using email as loginid for consistency
                mobile=mobile or '',
                password=password,
                status='activated' # Auto-activate for now, or keep as 'waiting'
            )
            
            return JsonResponse({'success': True, 'message': 'Registration successful'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').lower()
            password = data.get('password')
            
            user = UserRegistrationModel.objects.filter(email=email, password=password).first()
            
            if user:
                if user.status != 'activated':
                    return JsonResponse({'success': False, 'error': 'Account not activated'}, status=403)
                
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'mobile': user.mobile
                    }
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                 return JsonResponse({'success': False, 'error': 'Email required'}, status=400)

            # Check if it's a survey result
            if 'age' in data or 'risk' in data:
                UserSurveyPredictionModel.objects.create(
                    name=data.get('userName', 'User'),
                    email=email,
                    age=data.get('age', 0),
                    gender=data.get('gender', 0),
                    designation=data.get('designation', 0),
                    company_type=data.get('companyType', 0),
                    wfh_setup=data.get('wfhSetup', 0),
                    resource_allocation=data.get('resourceAllocation', 0.0),
                    mental_fatigue=data.get('mentalFatigue', 0.0),
                    stress_percentage=data.get('percentage', 0.0),
                    risk_level=data.get('risk', 'Low')
                )
            else:
                # Image-based results
                UserImagePredictionModel.objects.create(
                    username=data.get('userName', 'User'),
                    email=email,
                    loginid=email,
                    filename=data.get('filename', 'scan.jpg'),
                    emotions=data.get('emotion', 'Neutral'),
                    stress_level=data.get('stressLevel', 'Low'),
                    confidence=data.get('confidence', 0),
                    eye_strain=data.get('eyeStrain', 'Normal'),
                    brow_tension=data.get('browTension', 'Normal'),
                    facial_fatigue=data.get('facialFatigue', 'Normal'),
                )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
            
    elif request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'success': False, 'error': 'Email required'}, status=400)
            
        image_results = UserImagePredictionModel.objects.filter(email=email).order_by('-cdate')[:20]
        survey_results = UserSurveyPredictionModel.objects.filter(email=email).order_by('-cdate')[:20]
        
        combined = []
        for r in image_results:
            combined.append({
                'type': 'image',
                'id': r.id,
                'emotion': r.emotions,
                'stressLevel': r.stress_level,
                'confidence': r.confidence,
                'eyeStrain': r.eye_strain,
                'browTension': r.brow_tension,
                'facialFatigue': r.facial_fatigue,
                'timestamp': r.cdate.isoformat(),
                'method': 'Image Analysis'
            })
        
        for r in survey_results:
            combined.append({
                'type': 'survey',
                'id': r.id,
                'stressLevel': r.risk_level,
                'percentage': r.stress_percentage,
                'timestamp': r.cdate.isoformat(),
                'method': r.method if hasattr(r, 'method') else 'XGBoost Survey Prediction'
            })

            
        # Sort combined by timestamp
        combined.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return JsonResponse({'success': True, 'results': combined[:20]})
        
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

