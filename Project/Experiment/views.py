from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .models import Plate, Well
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class PlateCreateView(CreateView):
    model = Plate
    fields = ('name', 'type')

    def get_success_url(self):
        return reverse("Experiment:index")
    
    def form_valid(self, form):
        self.object = form.save(False)
        self.object.save()
        row_count = 24
        col_count = 16
        if self.object.type == "96":
            row_count = 12
            col_count = 8

        for row in range(row_count):
            for col in range(col_count):
                Well.objects.create(
                    # reagent="R"+'{:0d}'.format(self.object.id)+str(row)+str(col),
                    plate=self.object, row=row, col=col
                )
    
        return HttpResponseRedirect(self.get_success_url())


class PlateView(View):
    template_name = 'Experiment/home.html'

    def get(self, request):
        plates = Plate.objects.all().values('name', 'id')
        return render(request, self.template_name, {"plates": plates})
    
 
class PlateDeleteView(DeleteView):
    model = Plate
    success_url ="/"


class PlateDetailView(View):
    template_name = 'Experiment/detail.html'

    def get(self, request, plate_id):
        plate_name = Plate.objects.filter(id=plate_id).first().name
        wells = Well.objects.filter(plate__id=plate_id).values()
        for well in wells:
            well['color'] = "white"
            if well.get("reagent", "") != "" or well.get("antibody" ,"") not in ["empty", ""] or well.get("concentration", 0.0) != 0.0:
                well['color'] = "green"
            if well.get("plate__type", "") == "96":
                well['width'] = "12"
            else:
                well['width'] = "6"
        return render(request, self.template_name, {"wells": wells, "plate_name": plate_name, "plate_id": plate_id})


class WellView(View):
    template_name = 'Experiment/view_well.html'

    def get(self, request, well_id):
        well = Well.objects.filter(id=well_id).first()
        return render(request, self.template_name, {"well": well})
    
    
class WellUpdateView(UpdateView):
    model = Well
  
    fields = [
        "reagent",
        "antibody",
        "concentration"
    ]
    
    def get_success_url(self):
        object = self.get_object()
        return reverse("Experiment:view_well", kwargs={"well_id": object.pk})

    def form_valid(self, form):
        reagent_value = form.cleaned_data['reagent']
        concentration_value = form.cleaned_data['concentration']
        antibody_value = form.cleaned_data['antibody']

        reagent_validator = RegexValidator(
            regex=r'^R\d+$', 
            message='Reagent must start with "R" followed by numbers.',
            code='invalid_reagent'
        )

        if concentration_value < 0.0:
            form.add_error('concentration', 'Concentration should be non-negative')
            return self.form_invalid(form)

        if concentration_value > 0.0:
            if antibody_value == "empty" or antibody_value == "" or len(antibody_value) < 20 or len(antibody_value) > 40:
                form.add_error('antibody', "Concentration is only valid if there is also a antibody in the well and length of Antibody should be between 20 and 40")
                return self.form_invalid(form)
            
        if antibody_value != "empty" and antibody_value != "" and (len(antibody_value) < 20 or len(antibody_value) > 40):
            form.add_error('antibody', "Length of Antibody should be between 20 and 40")
            return self.form_invalid(form)
        
        aminoacid_lst = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "U", "O", "X", "B", "Z", "J", "Φ", "Ω", "Ψ", "π", "ζ", "+", "-"]
        if antibody_value != "empty" and antibody_value != "":
            if any(s not in aminoacid_lst for s in antibody_value):
                form.add_error('antibody', "The Antibody symbol is not valid, see https://en.wikipedia.org/wiki/Amino_acid for a list of valid 1-letter symbols")

        try:
            reagent_validator(reagent_value)
        except ValidationError as e:
            form.add_error('reagent', e)
            return self.form_invalid(form)
        
        return super().form_valid(form)