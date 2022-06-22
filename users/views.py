import json

import bcrypt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from users.models           import User
from core.validators         import (
    username_validate,
    email_validate,
    password_validate,
    phone_number_validate
)


class SignUpView(View):
    def post(self, requst):
        data = json.loads(requst.body)
        username     = data['username']
        password     = data['password']
        email        = data['email']
        phone_number = data['phone_number']
        last_name    = data['last_name']
        first_name   = data['first_name']
        nick_name    = data.get('adress')
        adress       = data.get('adress')

        username_validate(username)
        email_validate(email)
        phone_number_validate(phone_number)
        password_validate(password)        

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        if User.objects.filter(username = username).exists():
            return JsonResponse({'message' : 'Duplicated username'})        
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'message' : 'Duplicated email'})

        if User.objects.filter(phone_number = phone_number).exists():
            return JsonResponse({'message' : 'Duplicated phone number'})
        
        User.objects.create(
            username = username,
            pasword = hashed_password,
            email = email,
            phone_number = phone_number,
            last_name =last_name,
            first_name = first_name
        )