from rest_auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import serializers
from django.contrib.auth import get_user_model
import json


class CustomAPILoginView(LoginView):
    def get_response(self):
        """[CustomAPILoginView: Integrates JWT Token and User Details with LoginView]

        Returns:
            [object]: [JWT_TOKEN{}, USER{}, KEY]
        """
        # get original response from LoginView
        original_response = super().get_response()
        
        # remove key from original response and store in a variable to organize response order
        key = original_response.data.pop("key")
        
        # get logged in user data to provide in response
        user_data = {}
        user_qs = get_user_model().objects.filter(email=self.request.user.email)
        if user_qs.exists():
            user_data = json.loads(serializers.serialize('json', user_qs))[0].get("fields", {})
            # remove password from user_data
            del user_data["password"]
        
        # get refresh token for the logged in user
        refresh = RefreshToken.for_user(self.request.user)
        
        # customize response
        custom_response_data = {
            "jwt_token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "user": user_data,
            "key": key
        }
        # update original response
        original_response.data.update(custom_response_data)
        
        # return the response
        return original_response
