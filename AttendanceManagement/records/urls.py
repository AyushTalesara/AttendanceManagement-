from django.conf.urls import url
from . import views
app_name='test'
urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login_1,name='login'),
    url(r'^logout/$',views.logout_1,name='logout'),
    url(r'^enterdetails/$',views.enterdetails,name='enterdetails'),
    url(r'^teacherdetails/$',views.teacherdetails,name='teacherdetails'),
    url(r'^choice/$',views.fchoice,name='fchoice'),
    url(r'studentupdate/(?P<pk>[0-9]+)/$',views.StudentUpdate.as_view(),name='student-update'),
    url(r'teacherupdate/(?P<pk>[0-9]+)/$',views.teacherUpdate.as_view(),name='teacher-update'),
    url(r'studentdetails/(?P<id>[0-9]+)/$',views.StudentDetails,name='student-details'),
    url(r'detailsteacher/(?P<id>[0-9]+)/$',views.DetailsTeacher,name='details-teacher'),
    url(r'faceupdate/(?P<id>[0-9]+)/$',views.create_dataset,name='create_dataset'),
    url(r'^check/$',views.check,name='check'),




]
