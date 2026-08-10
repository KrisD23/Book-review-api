def test_get_books_requires_authentication(client):
    response = client.get("/books/")

    assert response.status_code == 401


def test_get_books_authenticated(client, auth_headers):
    response = client.get(
        "/books/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_create_book(client, auth_headers):
    response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Atomic Habits"
    assert body["author"] == "James Clear"
    assert "id" in body


def test_created_book_appears_in_book_list(client, auth_headers):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Deep Work",
            "author": "Cal Newport",
        },
    )

    assert create_response.status_code == 201

    list_response = client.get(
        "/books/",
        headers=auth_headers,
    )

    assert list_response.status_code == 200

    books = list_response.json()

    assert len(books) == 1
    assert books[0]["title"] == "Deep Work"
    assert books[0]["author"] == "Cal Newport"


def test_get_book_by_id(client, auth_headers):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    book_id = create_response.json()["id"]

    response = client.get(
        f"/books/{book_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == book_id
    assert body["title"] == "Clean Code"
    assert body["author"] == "Robert C. Martin"



def test_update_book(client, auth_headers):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Old Title",
            "author": "Old Author",
        },
    )

    book_id = create_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        headers=auth_headers,
        json={
            "title": "New Title",
            "author": "New Author",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == book_id
    assert body["title"] == "New Title"
    assert body["author"] == "New Author"



def test_delete_book(client, auth_headers):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Temporary Book",
            "author": "Temporary Author",
        },
    )

    book_id = create_response.json()["id"]

    response = client.delete(
        f"/books/{book_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/books/{book_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_user_cannot_get_another_users_book(
    client,
    auth_headers,
    second_user_auth_headers,
):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Private Book",
            "author": "Private Author",
        },
    )

    assert create_response.status_code == 201

    book_id = create_response.json()["id"]

    response = client.get(
        f"/books/{book_id}",
        headers=second_user_auth_headers,
    )

    assert response.status_code == 404



def test_user_cannot_update_another_users_book(
    client,
    auth_headers,
    second_user_auth_headers,
):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Original",
            "author": "Author",
        },
    )

    book_id = create_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        headers=second_user_auth_headers,
        json={
            "title": "Hacked",
            "author": "Hacked",
        },
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_book(
    client,
    auth_headers,
    second_user_auth_headers,
):
    create_response = client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Protected Book",
            "author": "Author",
        },
    )

    book_id = create_response.json()["id"]

    response = client.delete(
        f"/books/{book_id}",
        headers=second_user_auth_headers,
    )

    assert response.status_code == 404



def test_filter_books_by_author(client, auth_headers):
    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
        },
    )

    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Deep Work",
            "author": "Cal Newport",
        },
    )

    response = client.get(
        "/books/?author=James Clear",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 1
    assert books[0]["title"] == "Atomic Habits"
    assert books[0]["author"] == "James Clear"


def test_search_books(client, auth_headers):
    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
        },
    )

    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Deep Work",
            "author": "Cal Newport",
        },
    )

    response = client.get(
        "/books/?search=atomic",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 1
    assert books[0]["title"] == "Atomic Habits"


def test_search_books_by_author(client, auth_headers):
    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
        },
    )

    client.post(
        "/books/",
        headers=auth_headers,
        json={
            "title": "Deep Work",
            "author": "Cal Newport",
        },
    )

    response = client.get(
        "/books/?search=newport",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 1
    assert books[0]["author"] == "Cal Newport"



def test_sort_books_by_title_ascending(client, auth_headers):
    for title in ["Clean Code", "Atomic Habits", "Deep Work"]:
        response = client.post(
            "/books/",
            headers=auth_headers,
            json={
                "title": title,
                "author": "Test Author",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/books/?sort_by=title&sort_order=asc",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert [book["title"] for book in books] == [
        "Atomic Habits",
        "Clean Code",
        "Deep Work",
    ]


def test_sort_books_by_title_descending(client, auth_headers):
    for title in ["Clean Code", "Atomic Habits", "Deep Work"]:
        response = client.post(
            "/books/",
            headers=auth_headers,
            json={
                "title": title,
                "author": "Test Author",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/books/?sort_by=title&sort_order=desc",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert [book["title"] for book in books] == [
        "Deep Work",
        "Clean Code",
        "Atomic Habits",
    ]



def test_paginate_books(client, auth_headers):
    for title in [
        "Book A",
        "Book B",
        "Book C",
        "Book D",
        "Book E",
    ]:
        response = client.post(
            "/books/",
            headers=auth_headers,
            json={
                "title": title,
                "author": "Test Author",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/books/?sort_by=title&sort_order=asc&limit=2&offset=1",
        headers=auth_headers,
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 2

    assert [book["title"] for book in books] == [
        "Book B",
        "Book C",
    ]


def test_limit_cannot_be_zero(client, auth_headers):
    response = client.get(
        "/books/?limit=0",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_limit_cannot_exceed_100(client, auth_headers):
    response = client.get(
        "/books/?limit=101",
        headers=auth_headers,
    )

    assert response.status_code == 422



def test_offset_cannot_be_negative(client, auth_headers):
    response = client.get(
        "/books/?offset=-1",
        headers=auth_headers,
    )

    assert response.status_code == 422



def test_get_nonexistent_book_returns_404(client, auth_headers):
    response = client.get(
        "/books/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Book not found"
    }


def test_update_nonexistent_book_returns_404(client, auth_headers):
    response = client.put(
        "/books/999999",
        headers=auth_headers,
        json={
            "title": "Updated",
            "author": "Updated Author",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Book not found"
    }


def test_delete_nonexistent_book_returns_404(client, auth_headers):
    response = client.delete(
        "/books/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Book not found"
    }