from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from drf_spectacular.utils import extend_schema
# Create your views here.


@extend_schema(tags=['Child Contract'])
class ChildContractView(ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        print(f'self post {self} {request}')
        return super().post(request)



@extend_schema(tags=['Child Contract'])
class ChildContractUpdateStatusView(UpdateAPIView):
    @extend_schema(exclude=True)
    def post():
        pass

    @extend_schema(exclude=True)
    def patch():
        pass

    @extend_schema(
        methods=['put'],
        summary="Update child contract status",
        description="Description.",
        # request=BookSerializer,
        # responses={200: BookSerializer},
    )
    def put(self, request):
        print(f'self put {self} {request}')
        return super().put(request)

@extend_schema(tags=['Child Contract'])
class ChildContractDeleteView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)