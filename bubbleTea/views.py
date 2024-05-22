from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from .form import *
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime

#-------- Fonction de requête mysql : -------- 

def my_custom_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row




#-------- Page d'Acceuil : --------

def homepage(request):
    return render(request, 'homepage.html')



#-------- -------- -------- --------
#-------- PARTIE UTILISATEUR : -----
#-------- -------- -------- --------


#-------- Fonction d'inscription d'un nouvel utilisateur : --------

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
#--------------> Pour un mdp haché :
#--------------> {make_password(password)} à la place de {password}
            my_custom_sql(query)
            print(f"New user : {name} {firstname}")
            return redirect('connection')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})



#-------- Fonction de connexion d'un utilisateur existant : --------

def log(request):
    if request.method == 'GET':
        return render(request, 'connection.html', {'form': ConnectionForm})
    elif request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            query = f"SELECT * FROM user WHERE email='{email}'"
            user = my_custom_sql(query)

            if user and check_password(password, user[4]):

                # Pour stocker les informations de l'utilisateur dans la session :
                request.session['email'] = email 
                # request.session['name'] = user[1]  
                # request.session['firstname'] = user[2] 

                # On precise la partie payload et la clé secrete
                payload = {"user_id": user[0], "user_email": email}
                key = "secret"
                # On crée le token avec les infos du dessus
                encoded_jwt = jwt.encode(payload, key, algorithm="HS256")
                    # print("encoded_jwt", encoded_jwt)
                # On stocke le token dans le local storage pr pvr y acceder selon les pages 
                request.session['access_token'] = encoded_jwt
                    # print (request.session.get('access_token', encoded_jwt))


                print(f"User {email} connected")
                return redirect('profil')
            else:
                # On réaffiche le formulaire de connexion (si l'authentification échoue) :
                return render(request, 'connection.html', {'form': form})
        else:
            return render(request, 'connection.html', {'form': form})



#-------- Page profil de l'utilisateur : --------
#-------- Fonction d'affichage / de modification / de suppression du compte --------

def profil(request):
    if request.session['access_token']  :
        if request.method == 'GET':
            email = request.session.get('email', None)
            if email:
                query = f"SELECT * FROM user WHERE email='{email}'"
                user = my_custom_sql(query)
                name = user[1]
                firstname = user[2]
                # Pour transmettre l'e-mail au template :
                return render(request,'profil.html',
                    {'form':CustomUserCreationForm,
                    'email':email, 
                    'name': name,
                    'firstname' : firstname},)
            else:
                return redirect('connexion')
            # return render(request, 'profil.html',{'form':CustomUserCreationForm})
        if request.method == 'POST':
            email = request.session.get('email', None)
            if email:

                if 'modif' in request.POST :
                    form = CustomUserCreationForm(request.POST, request.FILES)
                    if form.is_valid():
                        print('test')
                        name = form.cleaned_data['name']
                        firstname = form.cleaned_data['firstname']
                        new_email = form.cleaned_data['email']
                        password = form.cleaned_data['password1']
                        picture = form.cleaned_data.get('picture')

                        query = f"UPDATE user SET name='{name}', firstname='{firstname}', email='{new_email}', password='{make_password(password)}', picture='{picture}' WHERE email='{email}';"
                        my_custom_sql(query)
                        
                        print(f"Update : '{name}', '{firstname}', '{email}', '{make_password(password)}', '{picture}")
                        return redirect('profil')
                        # return render(request, 'profil.html', {'form': form})

                if 'supp' in request.POST :
                    query = f"DELETE FROM user where email ='{email}';" 
                    my_custom_sql(query)
                    print("User deleted")
                    return redirect('inscription')                
            else:
                form = CustomUserCreationForm()
                return render(request, 'profil.html', {'form': form})

    else :
        return redirect('connection')                

#-------- -------- -------- --------
#--------  PARTIE ADMIN :   --------
#-------- -------- -------- --------



#-------- Fonction d'inscription d'un nouvel admin : --------

def adminRegister(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST, request.FILES)
        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            query = f'''INSERT INTO admin (pseudo, email, password)
                    VALUES ('{pseudo}', '{email}', '{make_password(password)}');'''
#--------------> Pour un hashed_mdp :
#--------------> {make_password(password)} à la place de {password}
            my_custom_sql(query)
            print(f"New admin : {pseudo}")
            return redirect('adminLogin')
    else:
        form = AdminCreationForm()
    return render(request, 'adminRegister.html', {'form': form})



#-------- Fonction de connexion d'un admin : --------

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
                print(f"Admin Connecté")
                return redirect('controlDashboard')
            
            else:
                return render(request, 'adminRegister.html', {'form': form})
        else:
            return render(request, 'adminRegister.html', {'form': form})



#-------- Fonction d'ajout d'un nouveau produit : --------

def addProduct(request):
    if request.method == 'GET':
        return render(request, 'addProduct.html',{'form':AddProductForm})
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            description = form.cleaned_data['description']        
            price = form.cleaned_data['price']
            picture = form.cleaned_data['picture']
            stock = form.cleaned_data['stock']

        query = f'''INSERT INTO product (identifier, description, price, picture, stock)
                    VALUES ('{identifier}', '{description}', '{price}', '{picture}', '{stock}');'''

        my_custom_sql(query)
        print(f"New product : {identifier}")
        return redirect('products')
    else:
        return render(request, 'addProduct.html', {'form': form})
    

    
#-------- Fonction de selection d'un produit à modifier ou supprimer : --------    

def selectProduct(request):
        if request.method == 'GET':
            return render(request, 'controlDashboard.html',{'form':SelectProductForm})
        if request.method == 'POST':
            form = SelectProductForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                identifier = form.cleaned_data['identifier']
            
                # Enregistrer les données en session 
                request.session['id'] = id
                request.session['identifier'] = identifier

                return redirect('updateProduct')
        else:
            return render(request, 'controlDashboard.html', {'form': SelectProductForm})
        


#-------- Fonction de modification / suppression d'un produit : --------

def updateProduct(request):
    if request.method == 'GET':
        id = request.session.get('id', None)
        if id:
        # Pour transmettre l'id au template :
            return render(request, 'updateProduct.html', {'form':UpdateProductForm})
        else:
            return redirect('controlDashboard')
    if request.method == 'POST':
        id = request.session.get('id', None)
        if id:
            if 'modify' in request.POST :
                form = UpdateProductForm(request.POST, request.FILES)
                print(form)
                # print("coucou")
                if form.is_valid():
                    identifier = form.cleaned_data['identifier']
                    description = form.cleaned_data['description']
                    price = form.cleaned_data['price']
                    picture = form.cleaned_data.get('picture')
                    stock = form.cleaned_data['stock']

                query = f"UPDATE product SET identifier='{identifier}', description='{description}', price='{price}', picture='{picture}', stock='{stock}' WHERE id='{id}';"
                my_custom_sql(query)
                
                print(f"Updated product : '{id}', '{identifier}'")

                return redirect('products')

            if 'delete' in request.POST :
               query = f"DELETE FROM product where id ='{id}';" 
               my_custom_sql(query)
               print("Product deleted")
               return redirect('products')
        else:
            # form= UpdateProductForm()
            print( form)
            return render(request, 'controlDashboard.html', {'form': form})


#-------- Afficher les utilisateurs : --------

def AllUsers(request):
    allUsers = User.objects.raw("SELECT * FROM user")

    return render(request, 'allUsers.html', {
        'allUsers': allUsers,
    })


#-------- -------- -------- --------
#--------  PARTIE ACHAT :   --------
#-------- -------- -------- --------

#-------- Fonction d'affichage des produits : --------

def AllProducts(request):
    allProducts = Product.objects.raw("SELECT * FROM product")

    return render(request, 'products.html', {
        'allProducts': allProducts,
    })

#-------- Fonction d'affichage d'un produit : --------

def oneProduct(request, id):
    oneProduct = Product.objects.raw(f"SELECT * FROM product WHERE id = {id}")
    print("print:", oneProduct)

    return render(request, 'oneProduct.html', {
        'oneProduct': oneProduct,
    })

#-------- Fonction panier : --------

# def addCart(request):
#     print('test')






