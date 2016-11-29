from rest_framework import mixins, status, viewsets
from rest_framework.generics import GenericAPIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class GenericView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin, 
                       GenericAPIView):
    """ 
    Concrete view for retrieving, updating or deleting a model instance. 
    """ 
    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs) 
 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 

    def put(self, request, *args, **kwargs): 
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        if self.request.method == 'GET':
            id = self.request.query_params.get('id', None)
        else:
            id = self.request.data.get('id',None)
        try:
            return self.get_queryset().get(id=id)
        except:
            raise NotFound("Requested object is not found")