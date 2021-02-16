from django.urls import path
from users import views

urlpatterns=[
    path('signup/', views.SignUp.as_view({'post':'create'}), name="signup"),

    path('login/', views.LoginView.as_view(), name = "login"),
    path('refresh-token/', views.RefreshToken.as_view(), name = "refresh_token"),
    path('revoke-token/',views.RevokeToken.as_view(), name='revoke_token'),

    path('update-password/',views.UpdatePassword.as_view(), name='update_password'),
    path('reset_password/', views.ResetPassword.as_view(), name="reset_password"),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),

    path('countries/', views.CountryList.as_view({'get':'list'}), name="countries_list"),
    path('countries/<int:id>/', views.CountryList.as_view({'get':'retrieve'}), name="country"),

    path('states/', views.StateList.as_view({'get':'list'}), name="state_list"),
    path('states/<int:id>/', views.StateList.as_view({'get':'retrieve'}), name="state"),

    path('countries/<int:country_id>/states/<int:state_id>/',views.CountryAndState.as_view(), name="get_state"),
    path('state-list/country/<int:country_id>/',views.CountryAndState.as_view(), name="state_list"),

    path('profile/',views.Profile.as_view({'get':'retrieve', 'put':'update'}), name="profile"),


    path('plans/',views.PlansView.as_view({'get':'list'}), name='plans_list'),
    path('plans/<int:id>/', views.PlansView.as_view({'get':'retrieve'}), name='plan'),

    path('subscriptions/',views.SubscriptionsView.as_view({'get':'list'}), name='subscriptions_list'),
    path('subscriptions/<int:id>/', views.SubscriptionsView.as_view({'get':'retrieve', 'put':'update'}), name='subscription'),

    path('transactions/', views.TransactionView.as_view({'get':'list'}), name="transaction_list"),
    path('transactions/<int:id>', views.TransactionView.as_view({'get':'retrieve'}), name="transaction"),
    ]