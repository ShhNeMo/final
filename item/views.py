from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy

def browse(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'browse.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    if request.method == 'POST':
        Reviewform = ReviewForm(request.POST)
        Replyform = ReplyForm(request.POST)

        if Reviewform.is_valid():
            review = Reviewform.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('item:detail', pk=pk)
        if Replyform.is_valid():
            review = Review.objects.get(id=request.POST.get('review_id'))
            reply = Replyform.save(commit=False)
            reply.user = request.user
            reply.save()
            review.replies.add(reply)
            review.save()
            return redirect('item:detail', pk=pk)
        return redirect('item:detail', pk=pk)
    else:
        Reviewform = ReviewForm()
        Replyform = ReplyForm()

        return render(request, 'detail.html', {
            'item': item,
            'related_items': related_items,
            'review_form': Reviewform,
            'reply_form': Replyform,
        })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'form.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'form.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
