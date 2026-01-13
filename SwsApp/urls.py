"""
URL configuration for SwsApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sws import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path("teams/", views.teams_from_api, name = "teams"),    
    path("teams/create/", views.create_team, name="create_team"),   
    path('teams/delete/<int:team_id>/', views.delete_team, name='delete_team'),        
    path("teams/<int:team_id>/", views.team_detail_from_api, name="get_team"),
    path("teams/edit/<int:team_id>/", views.edit_team, name="edit_team"),
    path('teams/<int:team_id>/trophies_by_season/', views.trophies_by_season, name='trophies_by_season'),

    path("trophies/", views.trophies_from_api, name = "trophies"),    
    path('trophies/create/', views.create_trophy, name='create_trophy'),
    path('trophies/delete/<int:trophy_id>/', views.delete_trophy, name='delete_trophy'),
    path('trophies/edit/<int:trophy_id>/', views.edit_trophy, name='edit_trophy'),

    # 🔥 TROPHIES BY SEASON (Django -> FastAPI -> HTML)
    path(
        'teams/<int:team_id>/trophies_by_season/',
        views.trophies_by_season,
        name='trophies_by_season'
    ),



]
