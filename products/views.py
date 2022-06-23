import json

from django.http  import JsonResponse
from django.views import View

from products.models import Category, SubCategory

class NavigatorView(View):
    def get(self, request):
        categories     = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        result  = []
        result2 = []

        for category in categories:
            result2 = []
            for sub_category in sub_categories.filter(category_id = category.id):
                result2.append({
                    'id'   : sub_category.name,
                    'name' : sub_category.name
                })
            result.append(
                {'category'    : category.id,
                'name'         : category.name,
                'sub_category' : result2
                }
            )

        return JsonResponse({'result' : result}, status = 200)