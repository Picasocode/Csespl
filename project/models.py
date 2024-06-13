# models.py

from django.db import models
from app.models import CustomUser

class Project(models.Model):
    PROJECT_TYPES = (
        ('Professional Training 1', 'Professional Training 1'),
        ('Interdisciplinary Project', 'Interdisciplinary Project'),
        ('Project Work', 'Project Work'),
    )

    SCOPE_CHOICES = (
        ('IEEE Conference', 'IEEE Conference'),
        ('Springer Conference ','Springer Conference'),
        ('Scopus Conference','Scopus Conference'),
        ('Scopus Journals', 'Scopus Journals'),
        ('SCI Journals','SCI Journals'),
        ('Patent','Patent'),
        
    )

    ACCEPTANCE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    )
    type = models.CharField(max_length=100, choices=PROJECT_TYPES)
    research_outcome = models.CharField(max_length=100, choices=SCOPE_CHOICES,)
    title = models.CharField(max_length=255)
    project_domain=models.CharField(max_length=255,default="Ex:AI,Deep Learning,Cyber Security ....")
    abstract=models.TextField(default="Maximum 500 Words",max_length=500)
    members = models.ManyToManyField(CustomUser, through='ProjectMember')
    guide = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='guided_projects')
    status = models.CharField(max_length=10, choices=ACCEPTANCE_STATUS_CHOICES, default='pending')
    denied_reason = models.TextField(default="Nil")
    def __str__(self):
        return self.title

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    class Meta:
        unique_together = ['project', 'member']

    def __str__(self):
        return f"{self.member.name} - {self.project.title}"


class Review(models.Model):
    STATUS_CHOICES = [
        ('not_verified', 'Not Verified'),
        ('verified', 'Verified'),
    ]

    project = models.ForeignKey('Project', related_name='reviews', on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    ppt = models.FileField(upload_to='ppts/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_verified')

    def __str__(self):
        return f'Review for {self.project.title} - {self.status}'
