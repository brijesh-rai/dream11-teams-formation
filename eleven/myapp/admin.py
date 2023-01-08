from django.contrib import admin
from django.contrib import messages
from .models import *

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name","team_code",'pos',"credit","is_playing","cap","v_cap")
    list_filter = (["team_code","is_playing",'pos'])
    search_fields = ['name']
    
    def mark_playing(modeladmin, request, queryset):
        queryset.update(is_playing = True)
        messages.success(request,"Selected Players marked as Playing!")
        
    def mark_not_playing(modeladmin, request, queryset):
        queryset.update(is_playing = False)
        messages.success(request,"Selected Players marked as not Playing!")
    
    def mark_not_cap(modeladmin, request, queryset):
        queryset.update(cap = False)
        messages.success(request,"Selected Players marked as not Captain!")
        
    def mark_not_v_cap(modeladmin, request, queryset):
        queryset.update(v_cap = False)
        messages.success(request,"Selected Players marked as not Vice Captains!")
        
    def mark_both_not_cvc(modeladmin, request, queryset):
        queryset.update(cap = False)
        queryset.update(v_cap = False)
        messages.success(request,"Selected Players marked as Neither Captain nor Vice Captain!")
        
    def mark_both_cvc(modeladmin, request, queryset):
        queryset.update(cap = True)
        queryset.update(v_cap = True)
        messages.success(request,"Selected Players marked as Captain and Vice Captain!")
        
    admin.site.add_action(mark_playing, "Mark Playing")
    admin.site.add_action(mark_not_playing, "Mark Not Playing")
    admin.site.add_action(mark_not_cap, "Mark Not Captain")
    admin.site.add_action(mark_not_v_cap, "Mark Not Vice Captain")
    admin.site.add_action(mark_both_not_cvc, "Mark neither Captain nor Vice Captain")
    admin.site.add_action(mark_both_cvc, "Mark both as Captain and Vice Captain")
    
    
    
admin.site.register(Team)
admin.site.register(Position)
admin.site.register(Player,PlayerAdmin)