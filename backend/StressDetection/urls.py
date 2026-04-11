"""StressDetection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import result_view
from StressDetection import views as mainView
from StressDetection import api_views  # Import API views
from users import views as usr
from users import api_views as user_api  # Import new user API views
from admins import views as admins
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path("", mainView.index, name="index"),
    path("index/", mainView.index, name="index"),
    path("logout/", mainView.logout, name="logout"),
    path("UserLogin/", mainView.UserLogin, name="UserLogin"),
    path("AdminLogin/", mainView.AdminLogin, name="AdminLogin"),
    path("UserRegister/", mainView.UserRegister, name="UserRegister"),
    path('result/', result_view, name='result'),

    # REST API Endpoints (for frontend integration)
    path("api/detect/", api_views.api_detect_stress, name="api_detect_stress"),
    path("api/knn-results/", api_views.api_knn_results, name="api_knn_results"),
    path("api/health/", api_views.api_health, name="api_health"),

    ### User Side Views
    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("UploadImageForm/", usr.UploadImageForm, name="UploadImageForm"),
    path("UploadImageAction/", usr.UploadImageAction, name="UploadImageAction"),
    path("UserEmotionsDetect/", usr.UserEmotionsDetect, name="UserEmotionsDetect"),
    path("UserLiveCameDetect/", usr.UserLiveCameDetect, name="UserLiveCameDetect"),
    path("UserKerasModel/", usr.UserKerasModel, name="UserKerasModel"),
    path("UserKnnResults/", usr.UserKnnResults, name="UserKnnResults"),
    path("api/survey-predict/", usr.SurveyPrediction, name="SurveyPrediction"),
    
    # New Modern Theme Frontend Routes Additions
    path("results/", usr.user_results_view, name="user_results"),
    path("settings/", usr.user_settings_view, name="user_settings"),
    path("survey/", usr.survey_prediction_view, name="survey_prediction"),
    
    # New JSON API endpoints for frontend
    path("api/register/", user_api.api_register, name="api_register"),
    path("api/login/", user_api.api_login, name="api_login"),
    path("api/results/", user_api.api_results, name="api_results"),
    
    # Admin API endpoints
    path("api/admin/users/", user_api.api_admin_get_users, name="api_admin_get_users"),
    path("api/admin/results/", user_api.api_admin_get_results, name="api_admin_get_results"),
    path("api/admin/update-status/", user_api.api_admin_update_status, name="api_admin_update_status"),
    path("api/admin/delete-user/", user_api.api_admin_delete_user, name="api_admin_delete_user"),
    path("api/admin/reset-password/", user_api.api_admin_reset_password, name="api_admin_reset_password"),
    path("api/admin/delete-all-results/", user_api.api_admin_delete_all_results, name="api_admin_delete_all_results"),

    # User Profile APIs
    path("api/user/update-profile/", user_api.api_user_update_profile, name="api_user_update_profile"),
    path("api/user/change-password/", user_api.api_user_change_password, name="api_user_change_password"),
    path("api/user/delete-account/", user_api.api_user_delete_account, name="api_user_delete_account"),

    ### Admin Side Views
    path("AdminLoginCheck/", admins.AdminLoginCheck, name="AdminLoginCheck"),
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path("admin-settings/", admins.admin_settings_view, name="admin_settings"),
    path("ViewRegisteredUsers/", admins.ViewRegisteredUsers, name="ViewRegisteredUsers"),
    path("AdminActivaUsers/", admins.AdminActivaUsers, name="AdminActivaUsers"),
    path("AdminStressDetected/", admins.AdminStressDetected, name="AdminStressDetected"),
    path("AdminKNNResults/", admins.AdminKNNResults, name="AdminKNNResults"),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)