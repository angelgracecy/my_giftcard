from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import GiftCard, Trade, Rating, User
from .forms import CustomUserCreationForm, GiftCardForm, RatingForm

def home(request):
    gift_cards = GiftCard.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'trading/home.html', {'gift_cards': gift_cards})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_giftcard(request):
    if request.method == 'POST':
        form = GiftCardForm(request.POST)
        if form.is_valid():
            gift_card = form.save(commit=False)
            gift_card.owner = request.user
            gift_card.save()
            messages.success(request, 'Gift card added successfully!')
            return redirect('my_giftcards')
    else:
        form = GiftCardForm()
    return render(request, 'trading/add_giftcard.html', {'form': form})

@login_required
def my_giftcards(request):
    gift_cards = GiftCard.objects.filter(owner=request.user)
    return render(request, 'trading/my_giftcards.html', {'gift_cards': gift_cards})

@login_required
def trade_giftcard(request, pk):
    gift_card = get_object_or_404(GiftCard, pk=pk)
    if gift_card.owner == request.user:
        messages.error(request, "You can't trade your own gift card!")
        return redirect('home')
    
    trade = Trade.objects.create(
        gift_card=gift_card,
        seller=gift_card.owner,
        buyer=request.user,
        status='pending'
    )
    messages.success(request, 'Trade request sent!')
    return redirect('home')

@login_required
def rate_user(request, user_id):
    rated_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = request.user
            rating.rated_user = rated_user
            rating.save()
            
            # Update user's average rating
            ratings = Rating.objects.filter(rated_user=rated_user)
            avg_rating = sum(r.rating for r in ratings) / len(ratings)
            rated_user.rating = avg_rating
            rated_user.total_ratings = len(ratings)
            rated_user.save()
            
            messages.success(request, 'Rating submitted successfully!')
            return redirect('user_profile', user_id=user_id)
    else:
        form = RatingForm()
    return render(request, 'trading/rate_user.html', {'form': form, 'rated_user': rated_user})
