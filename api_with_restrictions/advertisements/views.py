from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, \
    FavoritesSerializer
from advertisements.permissions import IsOwnerOrIsAdmin, IsNotOwner
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            filters = Q(creator=user, status__in=['DRAFT']) |\
                      Q(status__in=['OPEN', 'CLOSED'])
            queryset = Advertisement.objects.filter(filters)
            return queryset
        return Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsAdmin()]
        if self.action == 'favorites':
            return [IsAuthenticated()]
        if self.action == 'favorite':
            return [IsAuthenticated(), IsNotOwner()]
        return []

    def get_serializer_class(self):
        if self.action in ['favorite', 'favorites']:
            return FavoritesSerializer
        return AdvertisementSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        advertisement = self.get_object()
        user = request.user

        if request.method == 'POST':
            try:
                Favorite.objects.get(user=user, advertisement=advertisement)
                return Response('Объявление уже добавлено в избранное!')
            except ObjectDoesNotExist:
                favorite = Favorite.objects.create(
                    user=user, advertisement=advertisement
                )
                serializer = self.get_serializer(favorite)
                return Response(serializer.data)

        if request.method == 'DELETE':
            if Favorite.objects.all():
                try:
                    favorite = Favorite.objects.get(
                        user=user, advertisement=advertisement
                    )
                    favorite.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except ObjectDoesNotExist:
                    return Response('Объявления нет в списке избранных!!')
            else:
                return Response('Список избранных объявлений пуст!')

    @action(detail=False)
    def favorites(self, request):
        user = request.user
        favorites = Favorite.objects.all().filter(user=user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)
