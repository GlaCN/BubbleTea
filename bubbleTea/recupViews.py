from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth.hashers import make_password, check_password
# from .models import User
from django.db import connection

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
# from django.urls import reverse



def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            firstname = form.cleaned_data['firstname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            picture = form.cleaned_data.get('picture')

            query = f'''INSERT INTO user (name, firstname, email, password, picture)
                    VALUES ('{name}', '{firstname}', '{email}', '{make_password(password)}', '{picture}');'''
#--------------> Pour un hached_mdp :
#--------------> {make_password(password)} à la place de {password}
            my_custom_sql(query)
            print(f"New user : {name} {firstname}")
            return redirect('connection')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})



def adminRegister(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST, request.FILES)
        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            query = f'''INSERT INTO admin (pseudo, email, password)
                    VALUES ('{pseudo}, '{email}', '{make_password(password)}');'''
            my_custom_sql(query)
            print(f"New admin : {pseudo}")
            return redirect('adminLogin')
    else:
        form = AdminCreationForm()
    return render(request, 'adminRegister.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'connection.html',{'form':ConnectionForm})
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            query = f"SELECT * FROM user WHERE email='{email}'"
            user = my_custom_sql(query)
            print(user)
            if check_password(password,user[4]) == True :
                print(f"Connecté")
                # return HttpResponseRedirect('homepage/')
                return redirect('profil')
            
            else:
                return render(request, 'inscription.html', {'form': form})
        else:
            return render(request, 'inscription.html', {'form': form})


def adminLogin(request):
    if request.method == 'GET':
        return render(request, 'adminLogin.html',{'form':ConnectionForm})
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            query = f"SELECT * FROM admin WHERE email='{email}'"
            admin = my_custom_sql(query)
            print(admin)
            if check_password(password,admin[3]) == True :
                print(f"Connecté")
                return redirect('controlDashboard')
            
            else:
                return render(request, 'aminRegister.html', {'form': form})
        else:
            return render(request, 'adminRegister.html', {'form': form})



# def addProduct(request):
#     if request.method == 'GET':
#         return render(request, 'controlDashboard.html',{'form':AddProductForm})
#     if request.method == 'POST':
#         form = AddProductForm(request.POST)
#         if form.is_valid():
#             identifier = form.cleaned_data['identifier']
#             description = form.cleaned_data['description']        
#             price = form.cleaned_data['price']
#             picture = form.cleaned_data['picture']
#             stock = form.cleaned_data['stock']

#         query = f'''INSERT INTO product (identifier, description, price, picture, stock)
#                     VALUES ('{identifier}', '{description}', '{price}', '{picture}', '{stock}');'''

#         my_custom_sql(query)
#         print(f"New product : {identifier}")
#         return redirect('products')
#     else:
#         return render(request, 'controlDashboard.html', {'form': form})






# def connect(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         firstname = request.POST['firstname']
#         password = request.POST['password']

#         # Connexion à la base de données :
#         # query = "SELECT * FROM user WHERE name=%s AND firstname=%s AND password=%s"
#         # user = my_custom_sql(query, [name, firstname, password])
#         query = "SELECT * FROM user WHERE name=%s AND firstname=%s AND password=%s", [name, firstname, password]
#         user = my_custom_sql(query)
#         # user = authenticate(request, name=name, firstname=firstname, password=password)
#         if user is not None:
#             login(request, user)
#             print("Connection")
#             return redirect('home')
#         else:
#             # si les données entrées sont incorrectes: 
#             messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
#     return render(request, 'connection.html')


def my_custom_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row



# def connect(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         firstname = request.POST['firstname']
#         password = request.POST['password']

#         # Connexion à la bd :
#         query = "SELECT * FROM user WHERE name=%s AND firstname=%s AND password=%s"
#         user_data = User.objects.raw(query, [name, firstname, password])

#         for user in user_data:
#             # Authentification de l'utilisateur :
#             login(request, user)
#             print("Connexion réussie")
#             return redirect('home')

#         # Si les données entrées sont incorrectes: 
#         messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

#     return render(request, 'connection.html')

# def my_custom_sql(query, params):
#     with connection.cursor() as cursor:
#         cursor.execute(query, params)
#         rows = cursor.fetchall()  
#         # fetchall() récupérer tous les résultats
#     if rows: 
#         return rows[0]  
#         # Retourne la première ligne
#     else:
#         return None  
#         # Si aucune ligne n'a été trouvée




# def inscription(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # form.raw("INSERT INTO users (pseudo, email, mdp)")
#             # return redirect('connexion')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'inscription.html', {'form': form})




def profil(request):
    if request.method == 'GET':
        return render(request, 'profil.html',{'form':CustomUserCreationForm})
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            firstname = form.cleaned_data['firstname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            picture = form.cleaned_data.get('picture')

            query = f'''INSERT INTO user (name, firstname, email, password, picture)
                    VALUES ('{name}', '{firstname}', '{email}', '{make_password(password)}', '{picture}');'''
            my_custom_sql(query)
            print(f"Update : {name}', '{firstname}', '{email}', '{make_password(password)}', '{picture}")
        else:
            form = CustomUserCreationForm()
        return render(request, 'profil.html', {'form': form})


# @login_required
def coco(request):
    return render(request, 'coco.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

