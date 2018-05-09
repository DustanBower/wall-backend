from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework import viewsets

from posts.models import Post
from posts.serializers import PostSerializer
from posts.serializers import UserSerializer

from wall.settings import NOTIFICATION_EMAIL
from wall.settings import SEND_EMAIL


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        response = super().create(request, *args, **kwargs)

        # if we haven't thrown an exception by now, we are go for launch.
        if SEND_EMAIL:
            send_mail(
                'Welcome to the Wall!',
                'Leave messages anyone can see.  '
                'Read messages others have left.',
                NOTIFICATION_EMAIL,
                [email], 
                fail_silently=True) # need to return the created user
            
        return response
