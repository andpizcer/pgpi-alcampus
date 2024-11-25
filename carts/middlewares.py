import uuid

class CartSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()

        if 'cart_id' not in request.session:
            request.session['cart_id'] = str(uuid.uuid4())

        return self.get_response(request)
