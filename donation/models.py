from django.db import models
from django.conf import settings
import datetime
User = settings.AUTH_USER_MODEL

from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,)
    name = models.CharField(max_length=50, default=" ")
    profession = models.CharField(max_length=50, default=" ")
    country = models.CharField(max_length=50, default=" ")
    city = models.CharField(max_length=50, default=" ")
    area = models.CharField(max_length=50, default=" ")
    image = models.ImageField(upload_to='profilepic/images', default="")
    phone =models.CharField(max_length=15, default=" ")
    blood_group = models.CharField(max_length=10, default=" ")
    


    
    def __str__(self):
        return self.user.email
    
 

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
            super().save(force_insert, force_update, using, update_fields)


    # def next_donation_date(self):
    #     date = self.donation_date + datetime.timedelta(days=90)
    #     return date




class Donation_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hospital = models.CharField(max_length=50, default=" ")
    donation_date = models.DateField(auto_now_add=False, null=True)
    next_donation_date = models.DateField( null=True)

    def __str__(self):
        return self.user.email
    
    def total(self):
        return datetime.date(self.donation_date) + datetime.timedelta(days=90)
        

    def save(self):
        self.next_donation_date = self.total()
        super(Profile, self).save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
            super().save(force_insert, force_update, using, update_fields)
    # def get_deadline():
    #     return datetime.date(donation_date) + datetime.timedelta(days=90)
   

class FriendList(models.Model):
    
    friends = models.ManyToManyField(User, related_name="friends")
    user = models.OneToOneField(User,related_name="user", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email
        

    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list =self
        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user = removee)
        friends_list.remove_friend(remover_friends_list.user)

    def is_mutual(self,account):
        if account in self.friends.all():
            return True
        return False


class Friend_Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="receiver")
    is_accept = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.receiver.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user = self.receiver)
        print(receiver_friend_list)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            print(self.sender)
            sender_friend_list = FriendList.objects.get_or_create(user = self.sender)[0]
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_accept=False
                self.save()

    def decline(self):
        self.is_accept=False
        self.save()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=1000,null=True)
    image = models.ImageField(upload_to='user_post',null=True)
    date = models.DateField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.user.email   





class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=1000,null=True)
    image = models.ImageField(upload_to='user_post',null=True)
  
    date = models.DateField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.user.email   


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    comments = models.CharField(max_length=500,null=True)
    post = models.ForeignKey(UserPost ,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.user.email)



