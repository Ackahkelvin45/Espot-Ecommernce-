from ast import Return
from email.policy import default
from logging import exception
from pickle import FALSE
import re
from tkinter.messagebox import NO
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *




def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

   
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlisting(request):
    return render(request, "auctions/createlisting.html")

def savelisting(request):
 if request.method == "POST":
    try:
        title= request.POST['title']
        user = request.user 
        description = request.POST['description']
        category = request.POST['category']
        imageurl = request.FILES['imageurl']
        bid = Bid(price=int(request.POST['bid']), owner=user)
        bid.save()
    except :
        
     return render(request, "auctions/createlisting.html" ,{
      "message":"Enter Valid Information"})
  
    listing = Listing(name=title, descriptions=description, owner=user,bid = bid, isclosed = False, imageurl = imageurl, category = category)
    listing.save()
        
    return HttpResponseRedirect(reverse("index"))
       
 
  
def listingpage(request,listing_id):
    listing=Listing.objects.get(pk=listing_id)
    user=request.user
    owner=listing.owner
    true=listing.isclosed
    comment=Comments.objects.filter(listing=listing)
    if listing.isclosed==False:
   
      if owner==user:
        return render (request,"auctions/listingpage.html",{
        "listing":listing,
        "owner":True,
        "comments":comment
        })
      else:    
      
        return render (request,"auctions/listingpage.html",{
        "listing":listing,
        "owner":False,
        "comments":comment
   })
    else:
         return render (request,"auctions/listingpage.html",{
        "listing":listing,
        "owner":False,
        "true":true,
        "winner":f"item has been sold at {listing.bid.price}$ to {listing.bid.owner}"
                })
def index(request):
    listing=Listing.objects.filter(isclosed=False)

    
    return render(request, "auctions/index.html",{
        "listing":listing,
       
    })

def addtowatchlist(request,listing_id):
    
     watchlistitem=Listing.objects.get(pk=listing_id)
     watchlistsave=watchlist(listing=watchlistitem)
     watchlistsave.save()
     return HttpResponseRedirect(reverse("listingpage",args=(listing_id,)))

def watchlistpage(request):
    watchlistitems=watchlist.objects.all()
    return render(request,"auctions/watchlist.html",
    {"watchlist":watchlistitems
    })

def removewatchlist(request,watchlisting_id):
    watchlistitem=watchlist.objects.get(pk=watchlisting_id)
    watchlistitem.delete()
    return HttpResponseRedirect(reverse("watchlistpage",args=(None)) )

def bid(request,listing_id):
 
    if request.method=='POST':
     listing=Listing.objects.get(pk=listing_id)
     try:
        bid=int(request.POST['bid'])
        
        newbid=Bid(price=bid,owner=request.user)
     except:
        return render(request,"auctions/listingpage.html",{
                "listing":listing,
                "message":"Please enter a valid "
            })

    if  newbid.price >listing.bid.price:
          newbid.save()
          listing.bid=newbid
          listing.save()
          return render(request,"auctions/listingpage.html",{
            "listing":listing,
             "message":"your bid was successfully placed"
         })
     
    else:
            return render(request,"auctions/listingpage.html",{
                "listing":listing,
                "message":"your bid was lower than the current bid"
            })

def closeauction(request,listing_id):
    listing=Listing.objects.get(pk=listing_id)
    listing.isclosed=True
    listing.save()


    return  HttpResponseRedirect(reverse("index",args=(None)) )



def closedauctionpage(request):

 listing=Listing.objects.filter(isclosed=True)

 user=request.user
 listed=Listing.objects.all()
 if not listed :
    return render(request, "auctions/closedauctions.html")
 else:
  for  list in listed:
    if user==list.owner:
        owner=True
    else :
        owner=False
 return render(request, "auctions/closedauctions.html",{
        "listing":listing,
        "owner":owner
    })
    
def addcomment(request,listing_id):
    if request.method=='POST':
     comment=request.POST['comment']
     list=Listing.objects.get(pk=listing_id)
     newcomment=Comments(text=comment,writer=request.user,listing=list)
     newcomment.save()
     return HttpResponseRedirect(reverse("index",args=(None)))

def categorylisting(request):
    if request.method=='POST':
        categorys=request.POST['category']
        listings=Listing.objects.filter(category=categorys,isclosed=False)
        
        return render (request,"auctions/index.html",{
        "listing":listings
     })

def deletelisitng(request,listing_id):
    if request.method=='POST':
        listing=Listing.objects.filter(pk=listing_id)
        listing.delete()
      
        return HttpResponseRedirect(reverse("closedauctionspage"))

        
        
