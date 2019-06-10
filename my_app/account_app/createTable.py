from .models import create_model1,install
from django.db import models
from django.utils import timezone
def CreateNewMessage(name):
    fields = {
        "floor_id":models.AutoField(primary_key=True),
        "from_name": models.CharField(max_length=32),
        "to_floor": models.IntegerField(default=0),
        "to_name": models.CharField(max_length=32),
        "send_time": models.DateTimeField(default=timezone.now),
        "content": models.TextField(),
        }
    options = {'ordering': [
        "floor_id",
        "from_name",
        "to_floor",
        "to_name",
        "send_time",
        "content",
    ], 'verbose_name': 'valued customer', }
    custom_model = create_model1(name=name, fields=fields, options=options, app_label='my_app',
                                 module='models')
    install(custom_model)  # 同步到数据库中