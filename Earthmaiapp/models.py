from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GalleryImage(models.Model):
    title = models.CharField(max_length=100,default='')  
    imagepath=models.ImageField(upload_to="images/Tree/",default="")
    
class BeachImage(models.Model):
    title = models.CharField(max_length=100,default='')  
    imagepath=models.ImageField(upload_to="images/Beach/",default="")
    
class SocialImage(models.Model):
    title = models.CharField(max_length=100,default='')  
    imagepath=models.ImageField(upload_to="images/Social/",default="")

class AboutCard(models.Model):
    name = models.CharField(max_length=100,default="")
    title = models.CharField(max_length=100)
    description = models.TextField()
    imagepath = models.ImageField(upload_to="images/about/",default="")

class Advisor(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    detail=models.CharField(max_length=150)
    description = models.TextField()
    imagepath = models.ImageField(upload_to='images/advisor/',default="")

    

class Initiative(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    imagepath = models.ImageField(upload_to='images/initiatives/',default="" )
    link = models.URLField()

class InvolvementOption(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    button_text = models.CharField(max_length=50, default="Learn More")
    button_class = models.CharField(max_length=20, default="btn-primary")


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from datetime import timedelta, timezone
        return self.created_at >= timezone.now() - timedelta(minutes=10)
    
class PartnershipRequest(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"



# from django.db import models

# class Project(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     main_image = models.ImageField(upload_to='project_images/')
#     slug = models.SlugField(unique=True , blank=True)  # For URL identification

#     def __str__(self):
#         return self.title


# class ProjectImage(models.Model):
#     project = models.ForeignKey(Project, related_name='gallery_images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='project_gallery/')

#     def __str__(self):
#         return f"{self.project.title} - Image {self.id}"
    
# class DropdownItem(models.Model):
#     title = models.CharField(max_length=100)
#     link = models.CharField(max_length=100)

