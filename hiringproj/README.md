### How to run?

1. Clone the repository
2. Create a virtual environment, activate it and install the requirements
3. Run the following command:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

4. Create a superuser with the following command:

```bash
python manage.py createsuperuser
```

Then, enter your preferred username, email and password.

5. Open your browser and go to http://127.0.0.1:8000/
6. You can login with the user you just created.