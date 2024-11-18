from django.urls import path

from . import views

app_name = 'address'

urlpatterns = [
	path("", views.AddressListView, name="addresses"),
	path("session_update", views.AddressSessionView, name="address-session-update"),
	path("add/", views.add_address, name="add_address"),
	path("edit/<uuid:id>", views.edit_address, name="edit_address"),
	path("delete/<uuid:id>", views.delete_address, name="delete_address"),
	path("set_default/<uuid:id>", views.default_address, name="set_default"),
]