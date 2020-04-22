from django.urls import path
from . import views
app_name='community'

urlpatterns=[
    path('',views.review_list,name='review_list'),
    path('create/',views.review_create,name='review_create'),
    path('<int:review_id>/',views.review_detail,name='review_detail'),
    path('<int:review_id>/delete/',views.review_delete,name='review_delete'),
    path('<int:review_id>/update/',views.review_update,name='review_update'),
    path('<int:review_id>/comments/',views.comments_create,name='comments_create'),
    path('<int:review_id>/comments/<int:comment_id>/delete',views.comments_delete,name='comments_delete'),
    ]