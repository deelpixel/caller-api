from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializer import GlobalSerializer, RegisterUsersSerializer,SpamSerializer, UserSerializer
from .models import Global, RegisterUsers, Spam
from django.db.models import F,Q, Case, When, Value, IntegerField
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.

class RegisterUsersViews(APIView):
    def post(self, request):
       
        serializer = RegisterUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SpamViews(APIView):
    
    def post(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            phone=request.data["phone"]
            spam_obj=Spam.objects.filter(phone=phone).exists()
            serializer = SpamSerializer(data=request.data)
            if spam_obj==False:
            
                if serializer.is_valid():
                    
                    serializer.save()
                    isglobalpresent=Global.objects.filter(phone=phone).exists()
                    if (isglobalpresent==True):
                      Global.objects.filter(phone=phone).update(spam=F('spam')+1)
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Spam.objects.filter(phone=phone).update(spam=F('spam')+1)
                isglobalpresent=Global.objects.filter(phone=phone).exists()
                if (isglobalpresent==True):
                   Global.objects.filter(phone=phone).update(spam=F('spam')+1)
                return Response({"status": "success"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "error", "data":"Please provide a phone number"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    

    def get(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = RegisterUsers.objects.filter(id=payload['id']).first()
        print("test")
        print(user)

        queryset = Global.objects.all()
        name = request.query_params.get('name')
        phone = request.query_params.get('phone')
        
        if name is not None:
          queryset = queryset.filter(name__icontains=name).annotate(custom_order=Case(
                                                                    When(name__exact=name, then=Value(1)),
                                                                    When(name__startswith=f'{name} ', then=Value(2)),
                                                                    When(name__startswith=name, then=Value(3)),
                                                                    When(name__icontains=name, then=Value(4)),
                                                                    output_field=IntegerField(),
                                                                    )
                                                                ).order_by('custom_order').values("id","name","phone","spam").distinct()
          '''spam_find=Spam.objects.filter(phone=queryset[0]['phone']).values("spam")
          if len(spam_find)!=0:
            spam=spam_find[0]["spam"]'''
        
        elif phone is not None:
           phone="+"+phone
           
           registered = queryset.filter(phone=phone).filter(registered=True).values()
           
           if len(registered)==0:
               #phone="+"+phone
               queryset = queryset.filter(phone=phone).values("id","name","phone","spam")
           else:
               print("check")
               #phone="+"+phone
               queryset= RegisterUsers.objects.all()
               queryset = queryset.filter(phone=phone).values("id","name","phone","spam")
               queryset=list(queryset)
               queryset[0]['id']='1r'
               print(queryset)
        
        #queryset[0]['spam']=spam
        return Response({"status": "success", "data":queryset}, status=status.HTTP_200_OK)
        

class UserView(APIView):
    

    def get(self,request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        queryset = Global.objects.all()
        id = request.query_params.get('id')
        
        if id is not None :
           if  'r' not in id:
               #phone="+"+phone
               queryset = queryset.filter(id=id).values("id","name","phone")
               phone=queryset[0]["phone"]
               
           else:
              id=id[:-1]
              q=RegisterUsers.objects.filter(id=id).values()
              phone=q[0]["phone"]
              contact=Global.objects.filter(registeruser_id=payload['id'],phone=phone).values()
              if len(contact)!=0:   
                
                #phone="+"+phone
                queryset = RegisterUsers.objects.all()
                queryset = queryset.filter(id=id).values("id","name","phone","email")
                queryset=list(queryset)
                print(queryset)
                queryset[0]["contact name"]=contact[0]["name"]
                #queryset=queryset.append([0]({"contact name":contact[0]["name"]}))
              else:
                
                #phone="+"+phone
                queryset = RegisterUsers.objects.all()
                queryset = queryset.filter(id=id).values("id","name","phone")
           queryset=list(queryset)
           spam_find=Spam.objects.filter(phone=phone).values()
           spam=''
           if len(spam_find)!=0:
             spam=spam_find[0]["spam"]   
           queryset[0]["spam"]=spam

        return Response({"status": "success", "data":queryset}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
            phone = request.data['phone']
            password = request.data['password']

            user = RegisterUsers.objects.filter(phone=phone).first()

            if user is None:
                raise AuthenticationFailed('User not found!')

            if  user.password != password:
                raise AuthenticationFailed('Incorrect password!')

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()

            response.set_cookie(key='token', value=token, httponly=True)
            response.data = {
                'token': token
            }
            return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success'
        }
        return response