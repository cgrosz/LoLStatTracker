from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validations(self, data):
        errors = {}
        if data['formType'] == "loginForm":
            try:
                x = User.objects.get(email=data['email'])
                if not bcrypt.checkpw(data['password'].encode(),x.password.encode()):
                    errors['password'] = "Incorrect password"
            except:
                errors['email'] = "The email u entered is not registered on the site"
        else:
            if len(data['first_name']) < 2:
                errors["first_name"] = "First name name should be at least 2 characters"
            if len(data['last_name']) < 2:
                errors["last_name"] = "Last Name name should be at least 2 characters"
            EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            if not EMAIL_REGEX.match(data['email']):
                errors['email'] = "Please enter a valid email address"
            if len(data['password']) < 8:
                errors["password"] = "Password should be at least 8 characters"
            if data['password'] != data['confirm_password']:
                errors['confirm_password'] = "Passwords do not match"
            #check to make sure there is no email in the database that the user is trying to register with
            if len(User.objects.filter(email=data['email'])) > 0:
                errors['email'] = "This email is already in use"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    summoner_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    objects = UserManager()
