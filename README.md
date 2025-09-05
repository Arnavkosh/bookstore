# Django Bookstore (Stripe Checkout)

Feature set:
- Product catalog (Books)
- Search
- Cart (session-based)
- Checkout with Stripe
- Orders & Admin dashboard
- Image uploads for book covers

## Quick start

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env  # add your real keys
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the store and http://127.0.0.1:8000/admin/ for the dashboard.

### Add products
Use the admin to add Books with price and stock. Upload a cover image if you have one.

### Payments
Create Stripe test keys at https://dashboard.stripe.com/test/apikeys and put them in `.env`.
To capture webhooks locally:
```
stripe listen --forward-to localhost:8000/payment/webhook/
```
Copy the webhook secret into `.env`.

### Deploy (quick idea)
- Render / Railway: build with `pip install -r requirements.txt`, run `python manage.py migrate && gunicorn bookstore.wsgi:application`
- Set environment variables from `.env`
- Static files: `python manage.py collectstatic --noinput`

> Tip: For UPI/NetBanking etc. in India, you can integrate Razorpay later; the architecture allows swapping Stripe with another provider.
