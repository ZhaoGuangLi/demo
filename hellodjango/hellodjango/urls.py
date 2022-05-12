from django.contrib import admin
from django.urls import path, include
 
from hellodjango.views import show_index
from hellodjango.search import search_form, lipai, allure
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', show_index),
    path('lipaiapi/', lipai),
    path('', search_form),
    path("lipaiapi/reports/", allure)
]