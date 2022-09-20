from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createlisting/",views.createlisting,name="createnewlisting"),
    path("savelisting/",views.savelisting,name="savelisting"),
    path("listingpage/<int:listing_id>/",views.listingpage,name="listingpage"),
    path("watchlist/<int:listing_id>/",views.addtowatchlist,name="addtowatchlist"),
    path("watchlistpage/",views.watchlistpage,name="watchlistpage"),
    path("<int:watchlisting_id>/",views.removewatchlist,name="removefromwatchlist"),
    path("bid/<int:listing_id>/",views.bid,name="bidpage"),
    path("closeauction/<int:listing_id>",views.closeauction,name="closeauctionnow"),
    path("closedauctions",views.closedauctionpage,name="closedauctionspage"),
    path("comment/<int:listing_id>",views.addcomment,name="addcomments"),
    path("category",views.categorylisting,name="category"),
    path("deletlisting/<int:listing_id>",views.deletelisitng,name="deletelisting")
]
