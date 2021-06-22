from rest_framework import serializers
from .models import Profile,FriendList,Friend_Request,Post,Donation_Info,UserPost,Comments
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = "__all__"
        depth=1



class Donation_date_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Donation_Info
        fields = "__all__"
        depth=1





class FriendListSerializers(serializers.ModelSerializer):
    class Meta:
        model = FriendList
        fields = "__all__"


class Friend_Request_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Friend_Request
        fields = "__all__"



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'



class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = '__all__'
        
        


        


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
