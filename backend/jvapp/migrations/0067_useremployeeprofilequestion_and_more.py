# Generated by Django 4.0.7 on 2022-09-21 14:55

from django.db import migrations, models
import django.db.models.deletion


def add_questions(apps, schema_editor):
    EmployeeQuestion = apps.get_model('jvapp', 'UserEmployeeProfileQuestion')
    for question in [
        'What do you like most about working for $employer_name?',
        'How would you describe $employer_name\'s culture?',
        'What qualities are most important to succeed at $employer_name?'
    ]:
        EmployeeQuestion(text=question).save()


class Migration(migrations.Migration):

    dependencies = [
        ('jvapp', '0066_jobvyneuser_employment_start_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEmployeeProfileQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='useremployeeprofileresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jvapp.useremployeeprofilequestion'),
        ),
        migrations.AlterUniqueTogether(
            name='useremployeeprofileresponse',
            unique_together={('user', 'question')},
        ),
        migrations.RunPython(add_questions, atomic=True)
    ]