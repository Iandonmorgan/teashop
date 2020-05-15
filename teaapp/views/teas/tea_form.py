import sqlite3
from datetime import date
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from teaapp.models import Tea, TeaPackaging, Packaging
from ..connection import Connection
from .tea_detail import get_tea

def tea_form(request):
    if request.method == 'GET':
        template = 'teas/tea_form.html'
        return render(request, template)
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

def tea_edit_form(request, tea_id):
    if request.method == 'GET':
        tea = get_tea(tea_id)
        template = 'teas/tea_form.html'
        context = {
            'tea': tea,
        }
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE teaapp_tea
                SET flavor = ?
                WHERE id = ?
                """,
                    (
                        form_data['flavor'], tea_id,
                    ))

            return redirect('teaapp:home')