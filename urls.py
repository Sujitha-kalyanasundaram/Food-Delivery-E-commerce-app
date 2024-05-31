from django.urls import path
from foodapp import views
from food import settings
from django.conf.urls.static import static
from . import views
from .views import contact 


urlpatterns = [
    path('home',views.home),
    path('viewcart',views.viewcart),
    path('pdetails/<pid>', views.pdetails),
    path('contact/', contact, name='contact'),
    path('register',views.register),
    path('about',views.about),
    path('menu/', views.menu),
    path('logout/', views.logout_view),
    path('catfilter/<cv>',views.catfilter),
    path('login',views.home),
    path('addtocart/<pid>', views.addtocart),
    path('remove/<uid>',views.remove),    
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),
    path('search/', views.search_results, name='search_results'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)