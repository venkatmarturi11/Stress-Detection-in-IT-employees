from django.shortcuts import render
from django.contrib import messages
from users.models import UserRegistrationModel,UserImagePredictionModel
from .utility.AlgorithmExecutions import KNNclassifier

# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid.strip().lower() == 'admin' and pswd.strip().lower() == 'admin':
            from django.shortcuts import redirect
            return redirect('AdminHome')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admin-dashboard.html')


def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'UserRegistrations.html', {'data': data})


def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'UserRegistrations.html', {'data': data})

def AdminStressDetected(request):
    data = UserImagePredictionModel.objects.all()
    return render(request, 'admins/AllUsersStressView.html', {'data': data})

def AdminKNNResults(request):
    obj = KNNclassifier()
    df, accuracy, classificationerror, sensitivity, Specificity, fsp, precision = obj.getKnnResults()
    df.rename(
        columns={'Target': 'Target', 'ECG(mV)': 'Time pressure', 'EMG(mV)': 'Interruption', 'Foot GSR(mV)': 'Stress',
                 'Hand GSR(mV)': 'Physical Demand', 'HR(bpm)': 'Performance', 'RESP(mV)': 'Frustration', },
        inplace=True)
    data = df.to_html()
    return render(request, 'admins/AdminKnnResults.html',
                  {'data': data, 'accuracy': accuracy, 'classificationerror': classificationerror,
                   'sensitivity': sensitivity, "Specificity": Specificity, 'fsp': fsp, 'precision': precision})

# Modern UI additions
def admin_settings_view(request):
    return render(request, 'admin-settings.html', {})

