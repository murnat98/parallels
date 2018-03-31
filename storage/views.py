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
