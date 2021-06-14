from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Minutes
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


@method_decorator(login_required, name='dispatch')
class MinuteList(ListView):
    queryset = Minutes.objects.order_by('-publication_date')
    template_name = 'minutes/minutes.html'
    paginate_by = 4


class MinutesDetail(DetailView):
    model = Minutes
    template_name = 'minutes/minutesDetail.html'
