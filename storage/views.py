from urllib import parse

from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View

from storage.models import Storage


class KeyList(View):
    default_limit = 5

    def get(self, request):
        """
        Return key-value list in json format.
        """
        if 'limit' in request.GET:
            try:
                limit = abs(int(request.GET['limit']))
            except ValueError:
                limit = self.default_limit
        else:
            limit = self.default_limit

        pairs = Storage.objects.all()[:limit]

        storage = {pair.key: pair.value for pair in pairs}

        return JsonResponse(storage)


class Key(View):
    def get(self, request, key=None):
        try:
            pair = Storage.objects.get(key=key)

            key, value = pair.key, pair.value
        except Storage.DoesNotExist:
            key, value = 0, 0

        return JsonResponse({key: value})

    def post(self, request, key=None):
        if 'value' not in request.POST:
            return JsonResponse({'success': False, 'error': 'Value is empty'})

        storage = Storage(key=key, value=request.POST['value'])

        try:
            storage.save()
        except IntegrityError:
            pass

        return JsonResponse({'success': True})

    def put(self, request, key=None):
        try:
            storage = Storage.objects.get(key=key)
        except Storage.MultipleObjectsReturned:
            pass  # TODO: return error here

        put_data = parse.parse_qs(request.body)
        storage_value = put_data[b'value'][0].decode('utf-8')

        storage.value = storage_value

        try:
            storage.save()
        except IntegrityError:
            pass

        return JsonResponse({'success': True})

    def delete(self, request, key=None):
        storage = Storage.objects.filter(key=key).delete()

        try:
            storage.save()
        except IntegrityError:
            pass

        return JsonResponse({'success': True})
