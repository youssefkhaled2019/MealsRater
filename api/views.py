from rest_framework import viewsets,request, status
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer,UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    # permission_classes = (AllowAny,) #IsAuthenticated AllowAny
    permission_classes = (ActionBasedPermission,)
    action_permissions={
        IsAuthenticated: ('update', 'partial_update', 'destroy', 'list',),
        AllowAny: ('create',)
    }
    # A viewset that provides default `create()`, `retrieve()`, `update()`,
    # `partial_update()`, `destroy()` and `list()` actions.
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password']=make_password(serializer.validated_data.get('password'))
        serializer.save()
        # self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key, 
                }, 
            status=status.HTTP_201_CREATED)
    
    # def list(self, request, *args, **kwargs):
    #     response = {'message': 'You cant show  users '}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if (instance.id == request.user.id):
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['password']=make_password(serializer.validated_data.get('password'))
            serializer.save()
            # self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({
                'message': "your not owner", 
                })
        # this will return autor's data as a response 
        # return Response(AuthorSerializer(instance.parent).data)

    # https://stackoverflow.com/questions/73790207/how-to-override-the-update-action-in-django-rest-framework-modelviewset


class MealViewSet(viewsets.ModelViewSet):#CRUD
    queryset = Meal.objects.all()  #x
    serializer_class = MealSerializer #x

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            '''
            create or update 
            '''
            try:
             meal = Meal.objects.get(id=pk)
            except Meal.DoesNotExist:
                json = {
                    'result':'error',
                    'message': 'Meal Rate not found ',
                   
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            
            stars = int(request.data['stars'])
            if(not(1<=stars<=5)):
                json = {
                    'result':'error',
                    'message': 'Meal Rate must 1<= rate <=5 ',
                   
                }
                return Response(json , status=status.HTTP_400_BAD_REQUEST)
            user = request.user
            # print(user)
            # username = request.data['username']
            # user = User.objects.get(username=username)

            try:
                # update
                rating = Rating.objects.get(user=user.id, meal=meal.id) # specific rate 
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Updated',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_200_OK)

            except Rating.DoesNotExist:
               
                # create if the rate not exist 
                rating = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_201_CREATED)

        else:
            json = {
                'message': 'stars not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=True, methods=['put'])
    # def rate_meal(self, request, pk=None):
    #     json = {
                 
    #                 'message': 'put method  ',
                   
    #             }
    #     return Response(json , status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    

    #   A viewset that provides default `create()`, `retrieve()`, `update()`,
    #v `partial_update()`, `destroy()` and `list()` actions.
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)