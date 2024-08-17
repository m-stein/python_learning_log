from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    return render(request, template_name='learning_logs/index.html')


def topics(request):
    return render(request, template_name='learning_logs/topics.html',
                  context={'topics': Topic.objects.order_by('text')})


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render(request, template_name='learning_logs/topic.html',
                  context={'topic': topic, 'entries': topic.entry_set.order_by('-date_added')})


def new_topic(request):
    # if user data was submitted, process the data and return to other page
    if request.method == 'POST':
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
        else:
            print("Warning: form not valid")

    # else return an empty form for the user to fill in data
    return render(request, template_name='learning_logs/new_topic.html', context={'form': TopicForm()})


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    # if user data was submitted, process the data and return to other page
    if request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = topic
            entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        else:
            print("Warning: form not valid")

    # else return an empty form for the user to fill in data
    return render(request, template_name='learning_logs/new_entry.html',
                  context={'topic': topic, 'form': EntryForm()})


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)

    # if user data was submitted, process the data and return to other page
    if request.method == 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=entry.topic.id)
        else:
            print("Warning: form not valid")

    # else return an empty form for the user to fill in data
    return render(request, template_name='learning_logs/edit_entry.html',
                  context={'entry': entry, 'form': EntryForm(instance=entry)})