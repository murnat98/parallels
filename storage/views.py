from urllib import parse

from django.db import DatabaseError
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
            return self._get_success_response(False, 'Value is empty!')

        storage = Storage(key=key, value=request.POST['value'])

        try:
            storage.save()
        except DatabaseError as error:
            return self._get_success_response(False, self._get_database_error_string(error, key))

        return self._get_success_response(True)

    def put(self, request, key=None):
        try:
            storage = Storage.objects.get(key=key)
        except Storage.MultipleObjectsReturned:
            return self._get_success_response(False)
        except Storage.DoesNotExist:
            return self._get_success_response(False, 'Key %d does not exist!' % key)

        put_data = parse.parse_qs(request.body)

        if b'value' not in put_data:
            return self._get_success_response(False, 'Value is empty!')

        storage_value = put_data[b'value'][0].decode('utf-8')

        storage.value = storage_value

        try:
            storage.save()
        except DatabaseError as error:
            return self._get_database_error_string(error, key)

        return self._get_success_response(True)

    def delete(self, request, key=None):
        Storage.objects.filter(key=key).delete()

        return self._get_success_response(True)

    @staticmethod
    def _get_database_error_string(error, key=None):
        """
        Get the error string from error exception.
        :param error: error exception
        :return: error string
        :rtype: str
        """
        database_error_code = error.args[0]

        if database_error_code == 1264:
            return 'Too big key!'
        elif database_error_code == 1062:
            return 'Key %d already exists. Try with another key!' % key
        else:
            return 'Some error occurred. Please, try one more time!'

    @staticmethod
    def _get_success_response(success, error=None):
        """
        Return JsonResponse response in format success and error if success is False.
        :param success: True or False
        :param error: error string
        :return: Response accoring to format
        :rtype: JsonResponse
        """
        error = error or 'Some error occurred. Please, try later!'

        if success is True:
            return JsonResponse({'success': success})
        else:
            return JsonResponse({'success': success, 'error': error})
