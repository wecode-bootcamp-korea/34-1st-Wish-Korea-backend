import json

import jwt

from django.http  import JsonResponse
from django.views import View

from orders.models import *

class CartView(View):
    def get(self, request): 