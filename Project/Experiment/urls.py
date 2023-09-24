from django.urls import path
from .views import *

app_name = "Experiment"

urlpatterns = [
    path('', PlateView.as_view(), name="index"),
    path('create', PlateCreateView.as_view(), name="create"),
    path('delete/<int:pk>', PlateDeleteView.as_view(), name="delete"),
    path('detail/<int:plate_id>', PlateDetailView.as_view(), name="detail"),
    path('view_well/<int:well_id>', WellView.as_view(), name="view_well"),
    path('edit_well/<int:pk>', WellUpdateView.as_view(), name="edit_well")
]