from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('graph/', views.get_initial_graph),
    path('search/', views.search, name="search"),
    path('addnode/', views.add_node, name="addnode"),
    path('addnode/post/', views.add_node_api, name="add_node_api"),
    path('search/<str:entity>/graph/', views.get_graph),
    # path('index/', views.index, name="index"),
    # path('search/manager/', include('manager.urls'))

]
