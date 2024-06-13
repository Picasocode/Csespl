from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils.html import format_html
from django.db.models import Subquery, OuterRef,Count
from django.db import models
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['project', 'document', 'ppt', 'status']
    list_filter = ['status']
    search_fields = ['project__title']
    
    def has_view_permission(self, request, obj=None):
        # Allow superusers and staff to view reviews
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        # Allow superusers and staff to change reviews
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        # Allow superusers and staff to delete reviews
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        # Allow superusers and staff to add reviews
        return request.user.is_superuser or request.user.is_staff

admin.site.register(Review, ReviewAdmin)

class CustomUserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
            return f'{obj.register_no} | {obj.name} | {obj.department} '

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = CustomUser.objects.filter(role='Student')
        
    member = CustomUserModelChoiceField(queryset=CustomUser.objects.filter(role='Student'))

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    form = ProjectMemberForm
    extra = 1
    can_delete = True
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'accepted':
            pass
        return []

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMemberInline]
    ordering = ['title']
    list_display = [ 'get_members','type', 'research_outcome', 'status',]
    list_filter = ['type', 'research_outcome', 'status']
    search_fields = ['title', 'guide__username', 'members__username']
    fieldsets = (
        (None, {'fields': ('type','guide','research_outcome','title','project_domain','abstract','status','denied_reason')}),

    )
    def title_abstract(self, obj):
        return format_html("<div>{}</div><br><br><div style='font-size: 0.9em;'>{}</div>", obj.title, obj.abstract)
    title_abstract.short_description = 'Title with Abstract'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'guide':
            kwargs["queryset"] = CustomUser.objects.filter(role='Staff')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_guide(self, obj):
        return obj.guide.name if obj.guide else "-"
    get_guide.short_description = 'Guide'

    def get_members(self, obj):
        members_info = []
        members_info.append(f"<div style='font-weight: bold;'>Project Title: {obj.title}</div>")
        members_info.append("<div style='display: flex; flex-wrap: wrap;'>")
        for member in obj.members.all():
            if member.profile_picture and member.profile_picture.storage.exists(member.profile_picture.name):
                profile_picture_url = member.profile_picture.url
            else:
                profile_picture_url = "/static/admin/img/default_profile.png"  # Ensure this path is correct and the file exists

            member_info = f"""
        <div style='float:left;color:black; flex: 1 1 calc(33.33% - 4px);box-sizing: border-box; border: 1px solid #ccc; margin: 2px; padding: 10px;'>
            <img src='{profile_picture_url}' width='50' height='50' style='border-radius: 50%; margin-bottom: 10px;' /><br>
            <strong>{member.name}</strong><br>
            <p style="font-size:12px">Register No: {member.register_no}<br>
            Department: {member.department}</p>
        </div>
            """
            members_info.append(member_info)
        return format_html("".join(members_info))
    get_members.short_description = 'Members'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(guide=request.user) | Q(members=request.user)).distinct()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.guide == request.user or request.user in obj.members.all()
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.guide == request.user or request.user in obj.members.all()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.guide == request.user or request.user in obj.members.all()
        return False
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []  # Default readonly fields
        if obj:
            if obj.status and obj.status != 'pending':  # If status is set and not pending, make it readonly
                readonly_fields.append('status')
        if not request.user.is_superuser:
            if request.user.role == 'Student':
                readonly_fields.append('status')  # Students cannot edit status
            elif request.user.role == 'Staff':
                readonly_fields.append('guide')  # Staff cannot edit guide
                if obj and obj.status == 'pending':
                    pass  # Staff can edit status only if it's pending
                else:
                    readonly_fields.append('status') 
            if obj:
                if obj.status and obj.status == 'accepted':  # If status is set and not pending, make it readonly
                    readonly_fields=['type','guide','research_outcome','project_domain','status','denied_reason']
        return readonly_fields # Make status readonly if it's already set
   
    def save_model(self, request, obj, form, change):
        if not change and obj.guide:
            staff_projects_count = Project.objects.filter(guide=obj.guide).count()
            if staff_projects_count >= 6:
                raise ValidationError("A staff member can only accept up to 6 projects.")
        super().save_model(request, obj, form, change)

admin.site.register(Project, ProjectAdmin)
