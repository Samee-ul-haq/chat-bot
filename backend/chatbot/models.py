from django.db import models
import uuid

# Create your models here.

class ChatMessage(models.Model):
    # primary_key=True ensures that each user_id is unique and serves as the primary key for the model
    user_id=models.UUIDField(default=uuid.uuid4,primary_key=True) 
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class user_model(models.Model):
    user_id=models.ForeignKey(ChatMessage,on_delete=models.CASCADE) # ForeignKey to link with ChatMessage model
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)