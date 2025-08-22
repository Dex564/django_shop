from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Category, Product, Size

