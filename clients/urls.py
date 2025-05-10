from django.urls import path
from clients.views import (
    RegistrationView, 
    LoginView,
    LogoutView,
    ActivationView,

)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  
    path('reg/', RegistrationView.as_view(), name='reg'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activation/<str:username>/<str:code>', ActivationView.as_view(), name='activate'),
   
    
]