from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import get_dealerships, login_request, logout_request, registration_request, get_dealer_details, add_review
from django.views.generic import TemplateView

app_name = 'djangoapp'
urlpatterns = [
                  # route is a string contains a URL pattern
                  # view refers to the view function
                  path('', get_dealerships, name='index'),
                  # path for about view
                  path('about/', TemplateView.as_view(template_name='djangoapp/about.html'), name='about'),
                  # path for contact us view
                  path('contact/', TemplateView.as_view(template_name='djangoapp/contact.html'), name='contact'),
                  # path for registration
                  # path for login
                  path('registration/', registration_request, name='registration'),
                  path('login/', login_request, name='login'),
                  # path for logout
                  path('logout/', logout_request, name='logout'),

                  # path for add a review view
                  path('review/<int:dealer_id>/',
                       view=add_review, name='add_review'),

                  # path for dealer reviews view
                  path('dealer/<int:dealer_id>/',
                       view=get_dealer_details, name='dealer_details'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
