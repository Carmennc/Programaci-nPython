from django.urls import path
from . import views 

urlpatterns = [
    path('plantas/',views.get_plantas, name="get_plantas"),
    path('planta/', views.post_planta, name="post_planta"),
    path('planta/<str:id>/',views.handle_one_planta, name= "handle_one_planta"),
    path('v2/planta/<str:id>/', views.v2, name="v2_example"),
]
