from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from utils.mixins import CustomResponseMixin, ExceptionMixin


class CustomModelViewSet(ExceptionMixin, CustomResponseMixin, ModelViewSet):
    """
    Custom ModelViewSet
    """

    http_method_names = ['get', 'post', 'delete']

    def remove_serialize_fields(self, data):
        if self.remove_field_list:
            # for multiple fields in a list
            if isinstance(data, list):  # checking if type is list or dict
                for i in data:
                    for field_name in self.remove_field_list:
                        i.pop(field_name)
            else:
                for field_name in self.remove_field_list:
                    data.pop(field_name)
        return data

    def create(self, request, *args, **kwargs):
        mod_data = kwargs.get('mod_data', None)
        serializer = self.get_serializer(
            data=mod_data) if mod_data else self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.custom_response(message=kwargs.get('message', None), resp_status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.remove_serialize_fields(serializer.data))

        serializer = self.get_serializer(queryset, many=True)

        return self.custom_response(data=self.remove_serialize_fields(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.custom_response(data=self.remove_serialize_fields(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        mod_data = kwargs.get('mod_data', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=mod_data, partial=partial) if mod_data else self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.custom_response(message=kwargs.get('message', None))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return self.custom_response(message=kwargs.get('message', None))
