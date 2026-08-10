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