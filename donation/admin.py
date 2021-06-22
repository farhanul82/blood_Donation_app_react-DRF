from django.contrib import admin
from .models import Profile,FriendList,Friend_Request,Post,Donation_Info,UserPost,Comments
# Register your models here.
admin.site.register(Profile)
class FriendListAdmin(admin.ModelAdmin):
    list_filter=['user']
    list_display=['user']
    search_fields=['user']
    readonly_fields=['user']

    class Meta:
        model = FriendList

admin.site.register(FriendList,FriendListAdmin)

class Friend_Request_Admin(admin.ModelAdmin):
    
    list_display = ['sender','receiver']
    search_fields = ['sender_name', 'sender_email','receiver_name','receiver_email']

    class Meta:
        model = Friend_Request

admin.site.register(Friend_Request,Friend_Request_Admin)

admin.site.register(Post) 
admin.site.register(Donation_Info)
admin.site.register(UserPost)
admin.site.register(Comments)