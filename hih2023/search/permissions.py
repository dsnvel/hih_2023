from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from .models import UserProfile

call_command("makemigrations", "search")
call_command("migrate")

content_type = ContentType.objects.get(app_label='search', model='userprofile')

permission = Permission.objects.create(
    codename='can_read_files',
    name='Can read files',
    content_type=content_type,
)