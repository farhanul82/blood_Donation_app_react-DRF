from rest_framework import status
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.shortcuts import render
from rest_framework.serializers import Serializer
from .serializers import ProfileSerializers, FriendListSerializers, Friend_Request_Serializers, PostSerializer, UserPostSerializer,Donation_date_Serializers,CommentsSerializer
from account.models import UserAccount
from .models import Profile, Friend_Request, FriendList, Post, Donation_Info,UserPost,Comments
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from account.serializers import UserSerializer
User = get_user_model()


# Create your views here.


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

    def retrieve(self, request, pk=None):
        query = Profile.objects.get(id=pk)
        serializer = ProfileSerializers(query)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        profile_serializer = ProfileSerializers(
            data=request.data, partial=False)
        if profile_serializer.is_valid():
            profile_serializer.save(user=user)
            response_mesage = {"msg": "Created",
                               "data": profile_serializer.data}
            return Response(response_mesage)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        print(user.id)
        instance = Profile.objects.get(user=user.id)
        

        profile_serializer = ProfileSerializers(
            instance, data=request.data, partial=False)
        if profile_serializer.is_valid():
            profile_serializer.save()
            response_mesage = {"msg": "updated",
                               "data": profile_serializer.data}
            return Response(response_mesage)
        else:
            print('error', profile_serializer.errors)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request):
        profile = Profile.objects.get(user=user.id)
        return profile

    def list(self, request):
        user = self.request.user
        print(user)
        user_profile = Profile.objects.get(user=user.id)
       
        serializer = ProfileSerializers(user_profile)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        
        name = request.data['name']
        profession = request.data['profession']
        country = request.data['country']
        
        city = request.data['city']
        area = request.data['area']
        blood_group = request.data['blood_group']
        phone = request.data['phone']
        donation_date = request.data['donation_date']
        

        instance = self.get_object()

        profile_serializer = ProfileSerializers(
            instance, data=request.data, partial=False)
        if profile_serializer.is_valid():
            profile_serializer.save()
            response_mesage = {"msg": "updated",
                               "data": profile_serializer.data}
            return Response(response_mesage)
        else:
            
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileViewSet(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ProfileSerializers(data)
       
        return Response(serializer.data)


#


class UserViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        users = UserAccount.objects.all()

        serializer = UserSerializer(users, many=True)

        all_data = []
        for user in serializer.data:

            user_profile = Profile.objects.get(user__id=user['id'])

            user_profile_serializer = ProfileSerializers(user_profile)
            user['profile'] = user_profile_serializer.data
            all_data.append(user)
        return Response(all_data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class send_request(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        id = request.data['id']
        if id:
            receiver = UserAccount.objects.get(pk=id)
            try:
                friend_requests = Friend_Request.objects.filter(
                    sender_id=self.request.user.id, receiver_id=receiver.id)
                try:
                    for request in friend_requests:
                        if request.is_accept:
                            raise Exception("You already sent a  request")
                    friend_requests = Friend_Request(
                        sender_id=self.request.user.id,  receiver_id=receiver.id)
                    friend_requests.save()
                    response_mesage = {
                        'message': "request is  sent", "user": id}

                    return Response(response_mesage)
                except:
                    response_mesage = {
                        'error': False, 'message': "request is not sent", "user": id}

            except:
                friend_requests = Friend_Request(
                    sender_id=self.request.user.id,  receiver_id=receiver.id)
                friend_requests.save()
                response_mesage = {
                    'error': False, 'message': "you must be authenticated", "user": id, "sender": self.request.user.id}
                friend_requests.save(response_mesage)
                return Response(response_mesage)
        else:
            response_mesage = {'error': False, 'message': "you must be authenticated",
                               "user": user_id, "sender": self.request.user.id}
        return Response(response_mesage)


class friend_request_Viewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, **kwargs):
        user = self.request.user
        all_data = []
        account = UserAccount.objects.get(id=user.id)
        friend_requests = Friend_Request.objects.filter(
            receiver_id=account.id, is_accept=True)
        num_of_requests = friend_requests.count()
        print(num_of_requests)

        serializers = Friend_Request_Serializers(friend_requests, many=True)
        for requests in serializers.data:
            x = requests['sender']
            print(x)
            sender_profile = Profile.objects.filter(user__id=x)
            print(sender_profile)
            sender_profile_serializer = ProfileSerializers(
                sender_profile, many=True)
            requests['senderProfile'] = sender_profile_serializer.data
            all_data.append(requests)
        return Response(all_data)

        # all_data=[]
        # user = self.request.user
        # query = Friend_Request.objects.filter(receiver_id=user.id)
        # serializers = FriendRequestSerializers(query,many=True)
        # return Response(serializers.data)

        # if account==user:
        #     friend_requests = Friend_Request.objects.filter(receiver_id=account.id, is_accept=True)
        #     serializers = Friend_Request_Serializers(friend_requests,many=True)
        #     for requests in friend_requests:
        #         all_data.append(requests)
        # else:
        #     response_mesage =   {'error':False,'message':"you can't view another user's profile"}
        #     return Response(response_mesage)
        # return Response(all_data)


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class accept_request_Viewset(views.APIView):
#     authentication_classes=[JWTAuthentication ]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self,request):
#         user=self.request.user


#         sender_id = request.data['id']
#         print(sender_id)


#         friend_request = Friend_Request.objects.filter(sender=sender_id,is_accept=True)


#         sender = Profile.objects.filter(user__id=sender_id)


#         receiver_friend_list =  FriendList.objects.get(user__id = user.id)
#         print(receiver_friend_list)

#         sender_friend_list = FriendList.objects.get(user__id = sender.id)
#         print(sender_friend_list)


#         receiver_friend_list.add_friend(sender)
#         sender_friend_list.add_friend(user)
#         friend_request.is_accept=False
#         friend_request.save()

#         response_mesage={'msg':'Friend Request accepted'}
#         return Response(response_mesage)


#         # if frien_request_id:
#         #     friend_request = Friend_Request.objects.filter(id=friend_request_id)


#         #     if friend_request:
#         #         friend_request.accept()
#         #         response_mesage={'msg':'Friend Request accepted'}
#         #         return Response(response_mesage)
#         #     else:
#         #         response_mesage = {'msg':'something went wrong'}
#         #         return Response(response_mesage)

#         # else:
#         #     response_mesage={'msg':'unable to accept friend request'}
#         #     return Response(response_mesage)

#         # return Response(response_mesage)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class accept_request_Viewset(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        id = request.data['id']

        friend_request = Friend_Request.objects.get(id=id)
        print(friend_request)

        friend_request.accept()

        response_mesage = {'msg': 'Friend Request accepted'}
        return Response(response_mesage)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class Remove_friend_Viewset(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
       
        sender_id = request.data['id']
        sender = UserAccount.objects.get(pk=sender_id)
        user_friend_list = FriendList.objects.get(user=user)
        user_friend_list.unfriend(sender)
        response_mesage = {'msg': 'successfully unfriend your friend'}
        return Response(response_mesage)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class Decline_request_Viewset(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        print(user.id)
        friend_request_id = request.data['id']
        print(friend_request_id)

        friend_request = Friend_Request.objects.get(id=friend_request_id)
        print(friend_request)
        friend_request.decline()
        response_mesage = {'msg': 'Friend Request declined'}
        return Response(response_mesage)


class FriendsViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = self.request.user
        all_data = []

        friend = FriendList.objects.get(user=user)

        serializer = FriendListSerializers(friend)

        for user in serializer.data['friends']:

            profile = Profile.objects.filter(user__id=user)

            profile_serializer = ProfileSerializers(profile, many=True)

            all_data.append(profile_serializer.data)
        
        serializer.data['profile'] = all_data
        return Response(all_data)








class DonationInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    queryset = Donation_Info.objects.all()
    serializer_class = Donation_date_Serializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):

        user = self.request.user
        hospital = request.data['hospital']
        donatio_date = request.data['donation_date']
        print(hospital)
        print(donatio_date)

        doantion_Info = Donation_Info(user= user,hospital=hospital,donation_date=donatio_date)
        doantion_Info.save()
        serializer = Donation_date_Serializers(doantion_Info)
        print(serializer.data)
        return Response(serializer.data)



@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserPostViewset(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)
    
    
    
    def list(self,request):
        user=self.request.user
        post = UserPost.objects.filter(user=user)
         
        post_serilizer = UserPostSerializer(post,many=True)
        all_data = []
        for posts in post_serilizer.data:
            profile = Profile.objects.get(user__id=posts['user'])
             
            comments = Comments.objects.filter(post=posts['id'])
            comments_serilizer = CommentsSerializer(comments,many=True)
            print(comments_serilizer.data)
            profile_serializer = ProfileSerializers(profile)
            posts['profile']=profile_serializer.data
            posts['comments']=comments_serilizer.data

            for com in posts['comments']:
                profile = Profile.objects.get(user__id=com['user'])
                profile_serializer = ProfileSerializers(profile)
                com['profile']=profile_serializer.data

            # for com in comments_serilizer.data:
            #     profile = Profile.objects.get(user__id=com['user'])
            #     profile_serializer = ProfileSerializers(profile)
            #     com['profile']=profile_serializer.data
            #     posts['comments']=com

            all_data.append(posts)
        
        return Response(all_data)


    def create(self, request):
        user = self.request.user
        print(user)
        
        text = request.data['text']
        image = request.data['image']
        print(image)
        post = UserPost(user=user, text = text, image=image)
        post.save()
        serializer = UserPostSerializer(post)
        print(serializer.data)
        return Response(serializer.data)





class PostsViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
 
    def list(self,request):
        user=self.request.user
        friends = FriendList.objects.get(user=user)
        
        
        posts = UserPost.objects.all()
        print(posts)
        
        
        all_data=[]
        for x in friends.friends.all():
            
            for post in posts:

                if post.user==x:
                    
                    serializer = UserPostSerializer(post)
                    item = serializer.data
                    print(item)
                    

                    
                        
                    item_profile = Profile.objects.get(user__id = item['user'])
                    item_profile_srializer = ProfileSerializers(item_profile)
                    item['profile']=item_profile_srializer.data
                   
                    comments = Comments.objects.filter(post=item['id'])
                    comments_serilizer = CommentsSerializer(comments,many=True)
                    item['comments']=comments_serilizer.data
                    for com in item['comments']:
                        profile = Profile.objects.get(user__id=com['user'])
                        profile_serializer = ProfileSerializers(profile)
                        com['profile']=profile_serializer.data
                        
                    
 
                    all_data.append(item)
    
        return Response(all_data) 





@method_decorator(ensure_csrf_cookie, name='dispatch')
class PostView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(ensure_csrf_cookie, name='dispatch')
class CommentsViewset(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    queryset = Comments.objects.all()
    
    def list(self, request):
        comment = Comments.objects.all()
        comment_serializer = CommentsSerializer(comment, many =True)
        all_data=[]

        for comments in comment_serializer.data:
            profile = Profile.objects.filter(user__id=comments['user'])

            profile_serializer = ProfileSerializers(profile, many=True)
            comments['profile']=profile_serializer.data
            all_data.append(comments)
        return Response(all_data)

    def create(self, request):
        user = self.request.user
        print(user)
        data = request.data
        id = request.data['id']
        user_comment = request.data['comment']
        post = UserPost.objects.get(pk=id)
        comments = Comments(user=user,comments=user_comment,post=post)
        comments.save()
        comments_serializer = CommentsSerializer(comments)
        response_mesage={'msg':'your comment is done', 'comment':comments_serializer.data}
        return Response(response_mesage,comments_serializer.data)













@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
