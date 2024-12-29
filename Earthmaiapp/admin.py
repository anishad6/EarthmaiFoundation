from django.contrib import admin
from Earthmaiapp.models import GalleryImage,BeachImage,SocialImage,SocialImage,AboutCard,Advisor,Initiative,InvolvementOption,Donation,Volunteer,PartnershipRequest


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['id','imagepath']

class BeachImageAdmin(admin.ModelAdmin):
    list_display = ['id','imagepath']


class SocialImageAdmin(admin.ModelAdmin):
    list_display = ['id','imagepath']

class AboutCardAdmin(admin.ModelAdmin):
    list_display=["id","name","title","description","imagepath"]

class  AdvisorAdmin(admin.ModelAdmin):
    list_display=["id","name","designation","detail","description","imagepath"]

class InitiativeAdmin(admin.ModelAdmin):
    list_display=["id","title","description","imagepath","link"]

class InvolvementOptionAdmin(admin.ModelAdmin):
     list_display=["id","title","description","link","button_text","button_class"]


class DonationAdmin(admin.ModelAdmin):
    list_display=["id","user","amount","message","date"]

class VolunteerAdmin(admin.ModelAdmin):
    list_display=["id","name","email","phone","message","date"]

class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display=["id","company_name","contact_person","email","message","submitted_at"]





admin.site.register(GalleryImage,GalleryImageAdmin) 
admin.site.register(BeachImage,BeachImageAdmin)
admin.site.register(SocialImage,SocialImageAdmin)
admin.site.register(AboutCard,AboutCardAdmin)
admin.site.register(Advisor,AdvisorAdmin)
admin.site.register(Initiative,InitiativeAdmin)
admin.site.register(InvolvementOption,InvolvementOptionAdmin)
admin.site.register(Donation,DonationAdmin)
admin.site.register(Volunteer,VolunteerAdmin)
admin.site.register(PartnershipRequest,PartnershipRequestAdmin)



# from .models import Project, ProjectImage
# Register your models here.



# class ProjectImageInline(admin.TabularInline):
#     model = ProjectImage
#     extra = 1

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [ProjectImageInline]
#     prepopulated_fields = {'slug': ('title',)}


