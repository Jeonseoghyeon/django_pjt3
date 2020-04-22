from django.shortcuts import render,redirect,get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required
# Create your views here.
def review_list(request):
    reviews=Review.objects.order_by('-id')
    context={
        'reviews':reviews
    }
    return render(request,'community/review_list.html',context)


@login_required
def review_create(request):
    if request.method == 'POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.user=request.user
            review.save()
            return redirect('community:review_list')
    else:
        form=ReviewForm()
    context={
        'form':form
    }
    return render(request,'community/form.html',context)

def review_detail(request,review_id):
    review=get_object_or_404(Review,id=review_id)
    form=CommentForm()
    context={
        'review':review,
        'form':form,
    }
    return render(request,'community/review_detail.html',context)

@login_required
def review_update(request,review_id):
    review=Review.objects.get(pk=review_id)
    if request.method=='POST':
        form = ReviewForm(request.POST,instance=review)
        if form.is_valid():
            form.save()
            return redirect('community:review_detail',review_id)
    else:
        form = ReviewForm(instance=review)

    context={
        'form':form
    }
    return render(request,'community/form.html',context)

@login_required
def review_delete(request,review_id):
    if request.method=='POST':
        review = Review.objects.get(id=review_id)
        review.delete()
        return redirect('community:review_list')


@login_required
def comments_create(request,review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user=request.user
            comment.save()
    return redirect('community:review_detail',review_id)

@login_required
def comments_delete(request,review_id,comment_id):
    comment=get_object_or_404(Comment,id=comment_id)
    if request.user == comment.user:
        if request.method=='POST':

            comment.delete()
            return redirect('community:review_detail', review_id)
    else:
        return redirect('community:review_detail', review_id)