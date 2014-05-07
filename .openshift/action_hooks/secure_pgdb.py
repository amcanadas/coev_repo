#!/usr/bin/env python
import hashlib, imp, os, sys
import random

# This function creates per-deployment random keys;
def make_secure_key(key_length):
    # These are the legal password characters
    # as per the Django source code
    # (django/contrib/auth/models.py)
    chars  = 'abcdefghjkmnpqrstuvwxyz'
    chars += 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    chars += '23456789'

    # Create a random string the same length as the default
    rand_key = ''
    for _ in range(key_length):
        rand_key += random.choice(chars)

    # Set the value
    return rand_key

# Get database Users
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], os.environ['DJANGO_PROJECT_NAME']))

from django.contrib.auth.models import User

try:
    usr = User.objects.get(username__exact='admin')
except Exception:
    usr = User.objects.create_superuser('admin', 'admin@test.com', 'pass')
    usr.save()

# New password
new_pass = make_secure_key(12)

# Update the user admin password
usr.set_password(new_pass)
usr.save()

# Print the new password info
print("Django application credentials:\n\tuser: admin\n\tpwd: " + new_pass)