from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def _assert_allowed_to_access_topic(request, topic):
    if topic.owner != request.user:
        raise Http404


def index(request):
    return render(request, template_name='learning_logs/index.html')


@login_required
def topics(request):
    return render(request, template_name='learning_logs/topics.html',
                  context={'topics': Topic.objects.filter(owner=request.user).order_by('text')})


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    _assert_allowed_to_access_topic(request, topic)

    return render(request, template_name='learning_logs/topic.html',
                  context={'topic': topic, 'entries': topic.entry_set.order_by('-date_added')})


@login_required
def new_topic(request):
    # if user data was submitted, process the data and return to other page
    if request.method == 'POST':
        form = TopicForm(data=request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()
            return redirect('learning_logs:topics')
        else:
            print("Warning: form not valid")

    # else return an empty form for the user to fill in data
    return render(request, template_name='learning_logs/new_topic.html', context={'form': TopicForm()})


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    _assert_allowed_to_access_topic(request, topic)

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


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    _assert_allowed_to_access_topic(request, entry.topic)

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