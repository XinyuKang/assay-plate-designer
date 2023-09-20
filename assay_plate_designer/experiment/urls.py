from django.urls import path
from .views import PlateList, PlateCreate, PlateEdit


urlpatterns = [
    path('', PlateList.as_view(), name="index"),
    path('createPlate', PlateCreate.as_view(), name="createPlate"),
    path('editPlate/<int:id>/', PlateEdit.as_view(), name="editPlate")
]