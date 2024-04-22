from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import *
from import_export import resources
from django.utils.html import format_html 

#avoid default ID  when uploading csv and specify custom fields to upload  
class StudentRegistrationResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('age', 'fullname',)
        import_id_fields = ['fullname']  # Specify the field used as import identifier PK
   
      
class StudentAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class =StudentRegistrationResource
    list_display = ('fullname', 'age', 'Registered_date','z_score', 'z_score_badge')
    search_fields = ('fullname',)
    list_filter = ('Registered_date', 'Updated_date')
    list_per_page = 10   
    list_max_show_all = 10

    def z_score(self, obj):
        return obj.calculate_z_score()

    def z_score_badge(self, obj):
        z_score = obj.calculate_z_score()
        if z_score > 3 or z_score < -3:
            badge_color = 'red'
        else:
            badge_color = 'gray'
        return format_html('<span style="background-color: {0}; color: white; border-radius: 4px; padding: 2px 5px;">{1}</span>', badge_color, round(z_score, 2))

    z_score_badge.short_description = 'Z-score'

admin.site.register(Student,StudentAdmin, )