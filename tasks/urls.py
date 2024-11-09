from django.urls import path
from .views import TaskAPIView, SpecialTaskAPIView

urlpatterns = [

    # Task API yo'llari
    path('tasks/', TaskAPIView.as_view(), name='tasks_list_create'),  # GET va POST uchun api qilish qismi
    path('tasks-id/<int:pk>/', TaskAPIView.as_view(), name='tasks_update_delete'),  # PUT va DELETE uchun api qsimi

    # SpecialTask API yo'llari
    path('special-tasks/', SpecialTaskAPIView.as_view(), name='special_tasks_list_create'),   # GET va POST uchun api qilish qismi
    path('special-tasks-id/<int:pk>/', SpecialTaskAPIView.as_view(), name='special_tasks_update_delete'),   # PUT va DELETE uchun api qsimi
]
