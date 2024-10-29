from django.urls import path
from .views import TaskAPIView, SpecialTaskAPIView

urlpatterns = [
    
    # Task API yo'llari
    path('tasks/', TaskAPIView.as_view(), name='task_list_create'),  # GET va POST uchun
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task_update_delete'),  # PUT va DELETE uchun

    # SpecialTask API yo'llari
    path('special-tasks/', SpecialTaskAPIView.as_view(), name='special_task_list_create'),  # GET va POST uchun
    path('special-tasks/<int:pk>/', SpecialTaskAPIView.as_view(), name='special_task_update_delete'),  # PUT va DELETE uchun
]
