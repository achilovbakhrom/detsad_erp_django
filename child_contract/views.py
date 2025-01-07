from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from child_contract.serializers import CreateChildContractSerializer, ChildContractSerializer
from core.models import ChildContract

@extend_schema(tags=['Child Contract'])
class ChildContractView(ListAPIView):
    pass

@extend_schema(tags=['Child Contract'])
class RetrieveChildContractView(RetrieveAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChildContractSerializer
    lookup_field = 'id'
    

@extend_schema(tags=['Child Contract'])
class CreateChildContractView(CreateAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateChildContractSerializer

@extend_schema(tags=['Child Contract'])
class ChildContractUpdateStatusView(UpdateAPIView):
    http_method_names = ['put']

@extend_schema(tags=['Child Contract'])
class ChildContractDeleteView(DestroyAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id')
        contract = ChildContract.objects.get(id=id)
        contract.status = 'created'
        contract.save()
        return super().destroy(request, *args, **kwargs)