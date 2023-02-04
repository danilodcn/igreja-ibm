from django.contrib.auth.models import User

if User.objects.count() == 0:
    User.objects.create_superuser("ibm", "ibm@ibm.com", "senha")
