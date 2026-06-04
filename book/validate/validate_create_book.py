from datetime import date


def validate_create_book(data):
    title = data.get("title")
    author = data.get("author")
    price = data.get("price")
    quantity = data.get("quantity")
    published_date = data.get("published_date")

    if not title or not str(title).strip():
        return {"error": "Title is required"}

    if not author or not str(author).strip():
        return {"error": "Author is required"}

    if price is None:
        return {"error": "Price is required"}
    try:
        price = int(price)
        if price < 0:
            return {"error": "Price must be greater than or equal to 0"}
    except (TypeError, ValueError):
        return {"error": "Price must be an integer"}

    if quantity is None:
        return {"error": "Quantity is required"}
    try:
        quantity = int(quantity)
        if quantity < 0:
            return {"error": "Quantity must be greater than or equal to 0"}
    except (TypeError, ValueError):
        return {"error": "Quantity must be an integer"}
    if published_date:
        try:
            if not isinstance(published_date, date):
                date.fromisoformat(published_date)
        except (ValueError, TypeError):
            return {"error": "published_date must be in YYYY-MM-DD format"}
    return None