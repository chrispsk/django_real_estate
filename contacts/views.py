from django.shortcuts import render, redirect
from .models import Contacts
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contacts.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have made already an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contacts(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        #Send send_mail
        try:
            send_mail(
                'Property Listing Inquiry',
                'There has been an inquiry for ' + listing + '. Sign into admin panel',
                'danvan123887@gmail.com',
                [realtor_email, 'danvan123887@gmail.com'], #CC to realtor and my email
                fail_silently=False
            )
        except Exception:
            pass

        messages.success(request, 'Your request has been submitted, a team member will get back to you soon')
        return redirect('/listings/'+listing_id)
