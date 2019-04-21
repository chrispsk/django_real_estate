from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
def index(request):
    #filter(is_published=True) because oredr_by affect is_published option in database. I cannot unpublished
    listings = Listing.objects.order_by('-list_date').filter(is_published=True) #all() #Show only if is_published is True
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {'listings': paged_listings} #listings if I don't want paginator
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    #listing = Listing.objects.filter(listing_id)
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {'listing': listing}
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    #keywords (takes from description)..
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords) #ex. London pool #non-exact match
    #CITY (Exact match)
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city) #for case insensitive use exact
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) #lte less equal
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price) #lte less equal

    context = {
    'state_choices':state_choices,
    'bedroom_choices':bedroom_choices,
    'price_choices':price_choices,
    'listings': queryset_list,
    'values':request.GET
    }
    return render(request, 'listings/search.html', context)
