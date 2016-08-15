from django.conf.urls import url,include
from . import views

app_name='winker'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.personal_register, name="personal_reg"),
    url(r'^login/',views.login_user, name="login"),
    url(r'^logout/$',views.logout_user, name="logout"),
    url(r'^orgregister/$',views.org_register,name='org_register'),
    url(r'^profile/$',views.user_profile,name='user_profile'),
    url(r'^profile/user_privacy/$',views.user_profile_privacy,name='user_privacy'),
    url(r'^profile/settings/$',views.user_profile_settings,name='user_settings'),
    url(r'^profile/sign_control/$',views.user_profile_signature_control,name='user_signature_control'),
    url(r'^profile/workspace/$',views.user_profile_workspace,name='user_workspace'),
    url(r'^profile/profile_update/$',views.user_profile_update,name='user_profile_update'),
    url(r'^profile/personal_sign$',views.personal_signature,name='personal_signature'),
    url(r'^profile/pro_sign$',views.professional_signature,name='professional_signature'),
    url(r'^(?P<code>[0-9a-zA-Z]+)/$',views.code_search,name='search_code'),
    url(r'^qr_code/(?P<code>[0-9a-f]+)/$',views.show_qr_code,name='show_qr_code'),
    url(r'^bar_code/(?P<code>[0-9a-f]+)/$',views.show_bar_code,name='show_bar_code'),
    url(r'^ghost_window/(?P<key>[0-9a-f]+)/$',views.image_code_generator,name='ghost_window'),
    url(r'^flag_check$',views.test_flag,name='flag_check'),
    url(r'^flag_window/(?P<key>[0-9a-f]+)/$',views.flagwindow,name='flag_window'),
    url(r'^flag_submit/$',views.flag_raiser, name='flag_raiser'),
    url(r'^invalidate_sign/$',views.test_validity, name='validity_test'),
    url(r'^invalidate_sign_view/(?P<key>[0-9a-f]+)/$',views.invalidation_window, name='invalidation_page'),
    url(r'^invalidate$',views.invalidation_submit, name='invalidation_result'),
    url(r'^privacy_control$',views.privacy_control,name='privacy_control'),
    url(r'^org_admin/$',views.org_admin, name='org_admin'),
    url(r'^org_admin/profile_update/$',views.org_profile_update, name="org_profile_update"),
    url(r'^org_admin/staff$',views.org_staff_management,name="org_staff_management"),
    url(r'^org_admin/privacy$',views.org_profile_privacy,name="org_profile_privacy"),
    url(r'^org_admin/sign_control',views.org_signature_control,name="org_sign_control"),
    url(r'^sign_bank/(?P<operation>[a-z]+)$',views.purchase_window,name="sign_bank"),
]