from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, DeletionMixin
from .models import Plate, Well
from .forms import PlateForm
from django.urls import reverse_lazy

class PlateList(ListView):
    model = Plate
    template_name = 'experiment/index.html'
    context_object_name = 'plates'

class PlateCreate(CreateView):
    model = Plate
    form_class = PlateForm
    template_name = 'experiment/create_plate.html'
    success_url = reverse_lazy('index')

class PlateEdit(UpdateView, DeletionMixin):
    model = Plate
    form_class = PlateForm
    template_name = 'experiment/edit_plate.html'
    context_object_name = 'plate'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('index')

    def post(self, request, id, *args, **kwargs):
        if "confirm_delete" in self.request.POST:
            return self.delete(request, *args, **kwargs)
        else:
            return super(PlateEdit, self).post(request)