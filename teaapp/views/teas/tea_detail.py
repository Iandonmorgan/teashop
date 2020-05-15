import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from teaapp.models import Tea, TeaPackaging, Packaging, model_factory
from ..connection import Connection

def get_tea(tea_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_tea
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id tea_id,
            t.name,
            t.flavor,
            tp.longevity_in_months longevity,
            tp.id teapackaging_id,
            p.name packaging_name,
            p.handmade,
            p.production_location
        FROM teaapp_tea t
        JOIN teaapp_teapackaging tp ON tp.tea_id = t.id
        JOIN teaapp_packaging p ON p.id = tp.packaging_id
        WHERE t.id = ?
        """, (tea_id,))

        return db_cursor.fetchone()

def tea_detail(request, tea_id):
    if request.method == 'GET':
        tea = get_tea(tea_id)
        tea_packaging = get_teapackaging(tea_id)
        template_name = 'teas/tea_detail.html'
        context = {
            'tea': tea,
            'tea_packaging': tea_packaging
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM teaapp_teapackaging
                    WHERE id = ?
                """, (tea_id,))

            return redirect(reverse('teaapp:home'))

def get_teapackaging(tea_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TeaPackaging)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            tp.id tea_packaging_id,
            tp.longevity_in_months longevity,
            p.name packaging_name,
            p.production_location
        FROM
            teaapp_tea t
            LEFT JOIN teaapp_teapackaging tp ON t.id = tp.tea_id
            LEFT JOIN teaapp_packaging p ON tp.packaging_id = p.id
        WHERE
            t.id = ?
        """, (tea_id,))

        return db_cursor.fetchall()

def create_tea(cursor, row):
    _row = sqlite3.Row(cursor, row)

    tea = Tea()
    tea.id = _row["tea_id"]
    tea.name = _row["name"]
    tea.flavor = _row["flavor"]

    teapackaging = TeaPackaging()
    teapackaging.id = _row["teapackaging_id"]
    teapackaging.longevity = _row["longevity"]

    packaging = Packaging()
    packaging.name = _row["packaging_name"]
    packaging.handmade = _row["handmade"]
    packaging.production_location = _row["production_location"]

    tea.teapackaging = teapackaging
    tea.packaging = packaging

    return tea