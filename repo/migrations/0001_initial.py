# Generated by Django 4.0.1 on 2022-01-20 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_root', models.BooleanField(default=False)),
                ('is_shared', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HeirData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='repo.folder')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='repo.folder')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='repo.folder')),
            ],
        ),
    ]
