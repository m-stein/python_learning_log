from django.shortcuts import render
from .models import Topic


def index(request):
    return render(request, template_name='learning_logs/index.html')


def topics(request):
    return render(request, template_name='learning_logs/topics.html',
                  context={'topics': Topic.objects.order_by('date_added')})


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render(request, template_name='learning_logs/topic.html',
                  context={'topic': topic, 'entries': topic.entry_set.order_by('date_added')})