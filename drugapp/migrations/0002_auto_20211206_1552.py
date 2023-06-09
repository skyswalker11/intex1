# Generated by Django 3.2.8 on 2021-12-06 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescriber',
            name='id',
        ),
        migrations.AddField(
            model_name='prescriber',
            name='picture_path',
            field=models.ImageField(default='/photos/profile_male', upload_to='photos'),
        ),
        migrations.AlterField(
            model_name='prescriber',
            name='npi',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='prescriber',
            name='state',
            field=models.ForeignKey(db_column='state', on_delete=django.db.models.deletion.CASCADE, to='drugapp.state', to_field='state_abbrev'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='drug_id',
            field=models.ForeignKey(db_column='drug_id', on_delete=django.db.models.deletion.CASCADE, to='drugapp.drug'),
        ),
        migrations.AlterField(
            model_name='triple',
            name='npi',
            field=models.ForeignKey(db_column='npi', on_delete=django.db.models.deletion.CASCADE, to='drugapp.prescriber'),
        ),
    ]
