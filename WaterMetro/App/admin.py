from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Routes)
admin.site.register(Route_details)
admin.site.register(concession)
admin.site.register(concession_history)
admin.site.register(booking_history)
admin.site.register(PasswordReset)
admin.site.register(concession_discount)