from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView


class AddUniversityUnit(View):
    template_name = "university/add_item.html"

    def get(self, request):
        pass
        # if not request.user.has_perm('')

    def post(self, request):
        pass
