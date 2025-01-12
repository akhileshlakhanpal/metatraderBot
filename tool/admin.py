from django.contrib import admin

from .models import *

admin.site.register(server_details)
admin.site.register(master_details)
admin.site.register(copier_details)
