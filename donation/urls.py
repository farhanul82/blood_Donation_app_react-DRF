
from django.urls import path, include, re_path

from django.urls import path

from .views import UserViewSet,friend_request_Viewset,send_request,CommentsViewset,PostsViewSet,UserPostViewset,DonationInfoViewSet, FriendsViewSet,PostView,GetProfileViewSet,GetCSRFToken,Remove_friend_Viewset,ProfileViewSet,Decline_request_Viewset,accept_request_Viewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("donors", UserViewSet, basename='UserViewSet')
router.register("donorProfiles", ProfileViewSet, basename='ProfileViewSet')
router.register("userProfile", GetProfileViewSet, basename='GetProfileViewSet') 
router.register("requests", friend_request_Viewset, basename='friend_request_Viewset')
router.register("friends", FriendsViewSet, basename='FriendsViewSet')
router.register("donatonInfo", DonationInfoViewSet, basename='DonationInfoViewSet')
router.register("post", PostsViewSet, basename='PostsViewSet')
router.register("userPost", UserPostViewset, basename='UserPostViewset') 
router.register("comments", CommentsViewset, basename='CommentsViewset')

 
urlpatterns = [
    path('blood/', include(router.urls)),
    path('send_request/', send_request.as_view(),name='send_request'),
    path('requests_accept/', accept_request_Viewset.as_view(),name='requests_accept'),
    path('requests_decline/', Decline_request_Viewset.as_view(),name='decline_request'),
    path('remove_friend/', Remove_friend_Viewset.as_view(),name='Remove_friend'),
     path('posts/', PostView.as_view(), name= 'posts_list'),

    path('csrf_cookie', GetCSRFToken.as_view())
]
