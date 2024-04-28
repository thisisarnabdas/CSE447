from django.shortcuts import render, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

ENCRYPTION_KEY = os.urandom(16)


def encrypt_value(plaintext):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_plaintext)
    encrypted_value = b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_value


def decrypt_value(encrypted_value):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    encrypted_bytes = b64decode(encrypted_value.encode('utf-8'))
    decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)
    decrypted_value = unpad(decrypted_padded_bytes, AES.block_size).decode('utf-8')
    return decrypted_value


def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    context = {'variable1': 'this is sent', 'variable2': 'another variable'}
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        # Encrypt the email, first name, and last name
        encrypted_email = encrypt_value(email)
        encrypted_first_name = encrypt_value(first_name)
        encrypted_last_name = encrypt_value(last_name)

        try:
            user = User(
                email=encrypted_email,
                username=username,
                first_name=encrypted_first_name,
                last_name=encrypted_last_name,
                password=make_password(password)
            )
            user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'signup.html')

    return render(request, 'signup.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            return redirect('/')
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect("/login")


@login_required
def profile(request):
    user = request.user
    decrypted_email = decrypt_value(user.email)
    decrypted_first_name = decrypt_value(user.first_name)
    decrypted_last_name = decrypt_value(user.last_name)

    context = {
        'email': decrypted_email,
        'first_name': decrypted_first_name,
        'last_name': decrypted_last_name,
    }

    return render(request, 'profile.html', context)


def about(request):
    return render(request, 'about.html')
    # return HttpResponse("This is About Page")


def operators(request):
    return render(request, 'operators.html')
    # return HttpResponse("This is operators Page")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "You have successfully submitted the form.")

    return render(request, 'contact.html')


@login_required
@login_required
def create_encrypted_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Encrypt the title and content
        encrypted_title = encrypt_value(title)
        encrypted_content = encrypt_value(content)

        # Store the encrypted data in the session
        request.session['encrypted_title'] = encrypted_title
        request.session['encrypted_content'] = encrypted_content

        messages.success(request, "Your post has been submitted successfully.")
        context = {
            'encrypted_title': encrypted_title,
            'encrypted_content': encrypted_content,
            'show_decrypted': False,
        }
        return render(request, 'view_encrypted_post.html', context)

    return render(request, 'create_encrypted_post.html')


@login_required
def view_encrypted_post(request):
    encrypted_title = request.session.get('encrypted_title')
    encrypted_content = request.session.get('encrypted_content')

    if request.method == 'POST':
        show_decrypted = request.POST.get('show_decrypted') == 'true'
        if encrypted_title and encrypted_content:
            # Decrypt the title and content
            decrypted_title = decrypt_value(encrypted_title)
            decrypted_content = decrypt_value(encrypted_content)

            context = {
                'encrypted_title': encrypted_title,
                'encrypted_content': encrypted_content,
                'decrypted_title': decrypted_title,
                'decrypted_content': decrypted_content,
                'show_decrypted': show_decrypted,
            }
            return render(request, 'view_encrypted_post.html', context)

    if encrypted_title and encrypted_content:
        context = {
            'encrypted_title': encrypted_title,
            'encrypted_content': encrypted_content,
            'show_decrypted': False,
        }
        return render(request, 'view_encrypted_post.html', context)
    else:
        messages.error(request, "No encrypted post found.")
        return redirect('create_encrypted_post')