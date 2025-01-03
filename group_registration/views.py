from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Group Registration'])
class GroupRegistrationView(ListCreateAPIView):
    pass


@extend_schema(tags=['Group Registration'])
class GroupRegistrationUpdateStatusView(UpdateAPIView):
    
    @extend_schema(exclude=True)
    def post():
        pass
    
    @extend_schema(exclude=True)
    def patch():
        pass

@extend_schema(tags=['Group Registration'])
class GroupRegistrationDeleteView(DestroyAPIView):
    pass