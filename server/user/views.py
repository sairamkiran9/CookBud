from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, viewsets, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from user import serializers, models
from .models import RecipeRecommender
from .serializers import RecipeRecommenderSerializer
from .utils import RecSys

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    raise rest_exceptions.AuthenticationFailed(
        "Email or Password is incorrect!")


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")


@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"]=None
        
        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except models.User.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UserSerializer(user)
    return response.Response(serializer.data)

class RecipeRecommenderViewSet(viewsets.ModelViewSet):
    queryset = RecipeRecommender.objects.all()
    serializer_class = RecipeRecommenderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data)
    
    def retrieve(self, request, pk=None):
            queryset = self.queryset.filter(user=request.user, pk=pk).first()
            if not queryset:
                return response.Response({'error': 'Recipe not found'}, status=404)
            
            serializer = self.serializer_class(queryset)
            return response.Response(serializer.data)
        
    def create(self, request):
        ingredients = request.data.get('ingredients')
        spice_level = request.data.get('spice_level')
        cuisine_type = request.data.get('cuisine_type')
        recommendations = []

        if ingredients and spice_level:
            try:
                recommendations = RecSys(ingredients.split(', '), spice_level, cuisine_type, N=5)
                # Assuming RecSys returns a list of dicts with keys matching your model fields
                for rec in recommendations:
                    rec['user'] = request.user
                    RecipeRecommender.objects.create(**rec)
                serializer = RecipeRecommenderSerializer(recommendations, many=True)
                return response.Response(serializer.data)
            except Exception as e:
                return response.Response({'error': str(e)}, status=500)

        return response.Response({'error': 'Invalid input'}, status=400)

# @rest_decorators.api_view(['POST'])
# @rest_decorators.permission_classes([permissions.IsAuthenticated])
# def recommendationsView(request):
#     ingredients = request.data.get('ingredients')
#     spice_level = request.data.get('spice_level')
#     cuisine_type = request.data.get('cuisine_type')
#     recommendations = []

#     if ingredients and spice_level:
#         try:
#             recommendations = RecSys(ingredients.split(', '), spice_level, cuisine_type, N=5)
#             # Assuming RecSys returns a list of dicts with keys matching your model fields
#             for rec in recommendations:
#                 rec['user'] = request.user
#                 RecipeRecommender.objects.create(**rec)
#             serializer = RecipeRecommenderSerializer(recommendations, many=True)
#             return response.Response(serializer.data)
#         except Exception as e:
#             return response.Response({'error': str(e)}, status=500)

#     return response.Response({'error': 'Invalid input'}, status=400)