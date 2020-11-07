# Generated by Django 3.2 on 2020-10-31 14:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ResModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AdmEmail', models.CharField(max_length=50)),
                ('AdmPassword', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InsName', models.CharField(max_length=50)),
                ('InsField', models.CharField(max_length=50, null=True)),
                ('InsIntroduction', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='LitId',
            new_name='LiteratureId',
        ),
        migrations.RemoveField(
            model_name='search',
            name='CliEmail',
        ),
        migrations.AddField(
            model_name='collection',
            name='CollectionTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hubuser',
            name='UserImage',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hubuser',
            name='UserIntroduction',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='hubuser',
            name='UserPassword',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hubuser',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='UserEmail',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collection',
            name='UserEmail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail'),
        ),
        migrations.AlterField(
            model_name='hubuser',
            name='UserEmail',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UploadTime', models.DateTimeField(auto_now_add=True)),
                ('ReviewState', models.BooleanField()),
                ('ReviewTime', models.DateTimeField()),
                ('UserEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsClaim', models.BooleanField()),
                ('ResName', models.CharField(max_length=50)),
                ('ResEmail', models.CharField(max_length=50)),
                ('ResField', models.CharField(max_length=50, null=True)),
                ('ResIntroduction', models.CharField(max_length=50, null=True)),
                ('LiteratureNum', models.IntegerField()),
                ('CitedNum', models.IntegerField()),
                ('VisitNum', models.IntegerField()),
                ('ConcernNum', models.IntegerField()),
                ('ResCompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.institution')),
                ('UserEmail', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LiteratureNum', models.IntegerField()),
                ('ResearchId1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first', to='ResModel.researcher')),
                ('ResearchId2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second', to='ResModel.researcher')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MessageContent', models.CharField(max_length=2000)),
                ('MessageType', models.SmallIntegerField()),
                ('SendTime', models.DateTimeField(auto_now_add=True)),
                ('IsRead', models.BooleanField()),
                ('ReceiveEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MailContent', models.CharField(max_length=2000)),
                ('SendTime', models.DateTimeField(auto_now_add=True)),
                ('IsRead', models.BooleanField()),
                ('ReceiveEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive', to='ResModel.hubuser', to_field='UserEmail')),
                ('SendEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send', to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Concern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConcernTime', models.DateTimeField(auto_now_add=True)),
                ('ResearchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.researcher')),
                ('UserEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Browse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BrowseType', models.SmallIntegerField()),
                ('BrowseTime', models.DateTimeField(auto_now_add=True)),
                ('LiteratureId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ResModel.literature')),
                ('ResearchId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ResModel.researcher')),
                ('UserEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AppealState', models.BooleanField()),
                ('AppealTime', models.DateTimeField(auto_now_add=True)),
                ('ResearchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.researcher')),
                ('UserEmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ResModel.hubuser', to_field='UserEmail')),
            ],
        ),
    ]
