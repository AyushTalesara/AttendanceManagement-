# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import student,teacher,attendances,subjects
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(attendances)
admin.site.register(subjects)