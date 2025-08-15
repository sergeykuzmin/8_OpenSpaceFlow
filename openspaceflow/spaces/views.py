from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Space


class SpaceListView(ListView):
    model = Space


class SpaceDetailView(DetailView):
    model = Space


# def index(request):
# 	template_name = 'spaces/space_list.html'
# 	context = {
# 		'spaces': Space.objects.all(),
# 	}
# 	return render(request, template_name, context)
#
# def view(request, id):
# 	template_name = 'spaces/space_detail.html'
# 	context = {
# 		'space': Space.objects.get(pk=id),
# 	}
# 	return render(request, template_name, context)
