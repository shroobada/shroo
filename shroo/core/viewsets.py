from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with common functionality"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_serializer_class(self):
        """Allow different serializers for different actions"""
        if hasattr(self, 'serializer_classes'):
            return self.serializer_classes.get(self.action, self.serializer_class)
        return super().get_serializer_class()

    def get_permissions(self):
        """Allow different permissions for different actions"""
        if hasattr(self, 'permission_classes_by_action'):
            return [permission() for permission in
                    self.permission_classes_by_action.get(self.action, self.permission_classes)]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Get total count of objects"""
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        return Response({'count': count})

    def create(self, request, *args, **kwargs):
        """Enhanced create with better error handling"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        """Enhanced update with better error handling"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Base viewset for read-only operations"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    @action(detail=False, methods=['get'])
    def count(self, request):
        """Get total count of objects"""
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        return Response({'count': count})