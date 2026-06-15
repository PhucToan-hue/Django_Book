def filter_books(queryset, params):
    title = params.get('title')
    author = params.get('author')
    price = params.get('price')
    quantity = params.get('quantity')

    if title:
        queryset = queryset.filter(title__icontains=title)

    if author:
        queryset = queryset.filter(author__icontains=author)

    if price:
        try:
            price = int(price)
            queryset = queryset.filter(price=price)
        except ValueError:
            queryset = queryset.none()

    if quantity:
        try:
            quantity = int(quantity)
            queryset = queryset.filter(quantity=quantity)
        except ValueError:
            queryset = queryset.none()

    return queryset