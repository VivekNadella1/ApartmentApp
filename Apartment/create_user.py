from django.contrib.auth.models import User
# Create a new user
user = User.objects.create_user(username='john', password='password')

# Save the user to the database
user.save()