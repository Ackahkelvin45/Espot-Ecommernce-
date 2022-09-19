from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Bid (models.Model):
  price=models.IntegerField(default=0)
  owner=models.ForeignKey(User,on_delete=models.CASCADE,name="owner")
   




class Listing(models.Model):
  name=models.CharField(max_length=50)
  bid=models.ForeignKey(Bid,on_delete=models.CASCADE,related_name="bid")

  category=models.CharField(max_length=50)
  descriptions=models.CharField(max_length=200)
  isclosed=models.BooleanField(default=False)
  imageurl=models.ImageField(upload_to="images/")
  isclosed=models.BooleanField(default=False)
  owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner" ,null=True)
  def __str__(self):
    return f"{self.name } {self.bid} {self.category}"



class Comments(models.Model):
     text = models.CharField(max_length=800)
     writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
     listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")
     
     def __str__(self):
       return f"{self.text} {self.writer}"



class watchlist(models.Model):
 listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="watchlistlisting")

 
 