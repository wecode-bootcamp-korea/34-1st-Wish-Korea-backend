import jwt

from django.http  import JsonResponse

from users.models       import User
from wish_korea.settings import SECRET_KEY , ALGORITHM

def token_decorator(func):
    def wrapper(self,request,*args,**kwargs):
        try:
            access_token = request.headers.get("Authorization",None)
            # 헤더에있는 Aulthorization에서 value를 뽑아오고 없다면 None을 리턴한다.
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            # payload는 토큰속 사용자의 정보를 담고있는 곳이다.
            user = User.objects.get(id=payload['user_id'])
            # payload에 있는 user_id값을 DB와 대조시켜서 뽑아온다.
            request.user = user  
            # payload에 있는 user 정보와
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : ['INVALID_TOKEN'] }, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper