import sqlite3
from datetime import date
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from teaapp.models import Tea, TeaPackaging, Packaging
from ..connection import Connection

def tea_form(request):
    if request.method == 'GET':
        template = 'teas/tea_form.html'
        context = {
        }
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO teaapp_tea
        (
            name, flavor
        )
        VALUES (?, ?)
        """,
        (form_data['name'], form_data['flavor']))

    return redirect('teaapp:home')