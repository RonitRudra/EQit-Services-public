import re
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import (EmptyPage,
                                   PageNotAnInteger,
                                   Paginator)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.utils.timezone import now


from accounts.models import CustomUser, DEFAULT_ADDRESS
from gigs.forms import NewGigForm, NewGigLocationForm, NewGigTypeForm
from gigs.models import Gig, GigType, LikedGig, GigLocation, GigApproval
from postal.models import Message


# Create your views here.
class Home(TemplateView):
    template_name = "gigs/home.html"
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        return render(request,self.template_name)

class GigBrowse(TemplateView):
    template_name = 'gigs/gig_browse.html'

    def get(self, request, *args, **kwargs):

        gig_list = Gig.objects.filter(is_active=True).order_by('-date_posted')
        if gig_list.count() == 0:
            messages.add_message(request,messages.ERROR,'Sorry! No Gigs Available.')
            return redirect('gigs:home')
        page = request.GET.get('page',1)
        paginator = Paginator(gig_list,1)
        try:
            gigs = paginator.page(page)
        except PageNotAnInteger:
            gigs = paginator.page(1)
        except EmptyPage:
            gigs = paginator.page(paginator.num_pages)
        for gig in gigs:
            id  = gig.id
            gigtype= GigType.objects.get(gig_id = id)
            if request.user.is_provider:
                flag = True
                messages.add_message(request,messages.INFO,'As a provider, you do not have the ability to like/dislike gigs.')
            else:
                try:
                    liked = LikedGig.objects.get(user= request.user,gig=id)
                    flag = True
                except ObjectDoesNotExist:
                    flag = False
            field_names = [n.name for n in gigtype._meta.get_fields() if n.name != 'gig']
            values = [gigtype.__getattribute__(n) for n in field_names]
            gigtype = {k:v for k,v in zip(field_names,values)}

        return render(request,self.template_name,{'gigs':gigs,'gigtype':gigtype,'id':id,'flag':flag})

    def post(self, request, *args, **kwargs):

        # TODO: Check if row already exists, even though buttons are disabled for post requests.
        # Flag is True for like, false for dislike
        if request.POST['flag']:
            obj = LikedGig.objects.create(user=request.user,
                                          gig=Gig.objects.get(id=request.POST['gig_id']),status=True)
            messages.add_message(request,messages.INFO,'You LIKED a gig')
            
            # search for provider who posted the gig and send an automated message
            receiver = Gig.objects.get(id=request.POST['gig_id']).poster
            body = 'I Liked Your Gig'
            date_sent = now()
            new_message = Message.objects.create(sender=request.user,receiver=receiver,body=body,date_sent=date_sent)
            messages.add_message(request,messages.SUCCESS,'A message has been sent to the poster.')

        else:
            obj = LikedGig.objects.create(user=request.user,
                                          gig=Gig.objects.get(id=request.POST['gig_id']),status=False)
            messages.add_message(request,messages.INFO,'You DISLIKED a gig')
            #obj.save()
        return HttpResponseRedirect(request.path_info)

class GigNew(TemplateView):
    template_name = 'gigs/gig_new.html'

    def get(self, request, *args, **kwargs):
        ##
        user= CustomUser.objects.get(email=request.user)
        if user.is_provider==False:
            return redirect('gigs:home')
        ##
        form1 = NewGigForm(poster=None,prefix='form1')
        form2 = NewGigLocationForm(gig=None,prefix='form2')
        form3 = NewGigTypeForm(gig=None,prefix='form3')
        google_api_key = settings.GOOGLE_PLACES_API_KEY
        return render(request,self.template_name,{'form1':form1,'form2':form2,'form3':form3,'google_api_key':google_api_key})

    def post(self, request, *args, **kwargs):
        ##
        user= CustomUser.objects.get(email=request.user)
        if user.is_provider==False:
            return redirect('gigs:home')
        ##
        form1 = NewGigForm(poster=request.user,data=request.POST,prefix='form1')

        if form1.is_valid():
            gig = form1.save(commit=False)
            form2 = NewGigLocationForm(gig=gig,data=request.POST,prefix='form2')
            form3 = NewGigTypeForm(gig=gig,data=request.POST,prefix='form3')

        if form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()
            messages.add_message(request,messages.SUCCESS,'Your new gig has been posted!')
            return redirect('gigs:home')
        else:
            messages.add_message(request,messages.ERROR,'Something went wrong')
            return redirect('gigs:new-gig')

class ViewActivity(TemplateView):
    template_name = 'gigs/view_activity.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_provider:
            user_posted_gigs = Gig.objects.filter(poster=request.user).order_by('-date_posted')
            liked_gigs_others = LikedGig.objects.filter(gig_id__in=[i.id for i in user_posted_gigs]).order_by('-date_liked')
            gigs_pending_checkin = [i.gig for i in LikedGig.objects.filter(gig_id__in=[i.id for i in user_posted_gigs]).order_by('-date_liked') if i.gigapproval.is_checkin_requested==True]
            print(gigs_pending_checkin)
            return render(request,self.template_name,{'my_gigs':user_posted_gigs,'liked_gigs':liked_gigs_others,'gigs_pending_checkin':gigs_pending_checkin})
        else:
            liked_gigs_me = [i.gig for i in LikedGig.objects.filter(user = request.user, status=True).order_by('-date_liked')]
            approved_gigs = [i.gig for i in LikedGig.objects.filter(user = request.user).order_by('-date_liked') if i.gigapproval.is_approved == True]
            checkin_pending_gigs = [i.gig for i in LikedGig.objects.filter(user = request.user).order_by('-date_liked') if 
                                    i.gigapproval.is_approved == True and 
                                    i.gigapproval.is_checkin_requested==True and 
                                    i.gigapproval.is_checkin_approved==False]
            checkin_approved_gigs = [i.gig for i in LikedGig.objects.filter(user = request.user).order_by('-date_liked') if 
                                    i.gigapproval.is_approved == True and 
                                    i.gigapproval.is_checkin_requested==True and 
                                    i.gigapproval.is_checkin_approved==True and 
                                    i.gigapproval.is_completed==False]
            completed_gigs = [i.gig for i in LikedGig.objects.filter(user = request.user).order_by('-date_liked') if 
                                    i.gigapproval.is_approved == True and 
                                    i.gigapproval.is_checkin_requested==True and 
                                    i.gigapproval.is_checkin_approved==True and 
                                    i.gigapproval.is_completed==True]
            paid_gigs = [i.gig for i in LikedGig.objects.filter(user = request.user).order_by('-date_liked') if 
                                    i.gigapproval.is_paid== True]
            return render(request,self.template_name,{'liked_gigs':liked_gigs_me,
                                                      'approved_gigs':approved_gigs,
                                                      'checkin_pending_gigs':checkin_pending_gigs,
                                                      'checkin_approved_gigs':checkin_approved_gigs,
                                                      'completed_gigs':completed_gigs,
                                                      'paid_gigs':paid_gigs})

class GigDetail(DetailView):
    template_name = 'gigs/gig_detail.html'
    model = Gig

    # Override to pass api key as well
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_GEOCODE_API_KEY
        return context

class GigManage(TemplateView):
    template_name= 'gigs/gig_manage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_provider:
            return render(request,self.template_name,{'gig': Gig.objects.get(id=kwargs['pk'])})
        else:
            return redirect('gigs:home')

class GigManageApproval(TemplateView):
    template_name= 'gigs/gig_manage_approval.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_provider:
            # pk is passed by url dispatcher which extracted the regex from url
            # this is passed as kwargs eg, pk=pk_value where key is the name in (?P<name>pattern) in urlpattern
            # Only show gigs posted by provider
            users_liked = [i.user for i in LikedGig.objects.filter(gig=kwargs['pk']) if 
                           i.gig.poster == request.user and 
                           i.gigapproval.is_approved==False]
            return render(request,self.template_name,{'users_liked':users_liked,'gig_id':kwargs['pk']})
        else:
            return redirect('gigs:home')

    def post(self, request, *args, **kwargs):
        gig_id = request.POST['gig_id']
        gig_obj = Gig.objects.get(id=gig_id)
        for key,val in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'gig_id':
                obj = LikedGig.objects.get(user=val,gig=gig_id).gigapproval
                obj.is_approved = True
                obj.save()
                receiver = CustomUser.objects.get(id=val)
                body = 'Approved your interest for: {}'.format(gig_obj.title)
                date_sent = now()
                new_message = Message.objects.create(sender=request.user,receiver=receiver,body=body,date_sent=date_sent)
        
        messages.add_message(request,messages.SUCCESS,'Approved Participants have been notified!')
        return redirect('gigs:view-activity')

class GigManageCheckin(TemplateView):
    template_name= 'gigs/gig_manage_checkin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_provider:
            users_checkin = [i.user for i in LikedGig.objects.filter(gig=kwargs['pk']) if 
                           i.gig.poster == request.user and 
                           i.gigapproval.is_approved==True and 
                           i.gigapproval.is_checkin_requested==True and 
                           i.gigapproval.is_checkin_approved==False]
            return render(request,self.template_name,{'users_checkin':users_checkin,'gig_id':kwargs['pk']})
        else:
            return redirect('gigs:home')

    def post(self, request, *args, **kwargs):
        gig_id = request.POST['gig_id']
        gig_obj = Gig.objects.get(id=gig_id)
        for key,val in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'gig_id':
                obj = LikedGig.objects.get(user=val,gig=gig_id).gigapproval
                obj.is_checkin_approved = True
                obj.save()
                receiver = CustomUser.objects.get(id=val)
                body = 'You have been checked in for: {}'.format(gig_obj.title)
                date_sent = now()
                new_message = Message.objects.create(sender=request.user,receiver=receiver,body=body,date_sent=date_sent)
        
        messages.add_message(request,messages.SUCCESS,'Checked-in Participants have been notified!')
        return redirect('gigs:view-activity')

class GigManagePayment(TemplateView):
    template_name= 'gigs/gig_manage_payment.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_provider:
            users_payment = [i.user for i in LikedGig.objects.filter(gig=kwargs['pk']) if 
                           i.gig.poster == request.user and 
                           i.gigapproval.is_approved==True and 
                           i.gigapproval.is_checkin_requested==True and 
                           i.gigapproval.is_checkin_approved==True and 
                           i.gigapproval.is_paid==False]
            return render(request,self.template_name,{'users_payment':users_payment,'gig_id':kwargs['pk']})
        else:
            return redirect('gigs:home')

    def post(self, request, *args, **kwargs):
        gig_id = request.POST['gig_id']
        for key,val in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'gig_id':
                obj = LikedGig.objects.get(user=val,gig=gig_id).gigapproval
                # need to actually transfer tokens
                try:
                    gig_obj = Gig.objects.get(id=gig_id)
                    print(val)
                    payee = CustomUser.objects.get(id=val).wallet
                    payer = CustomUser.objects.get(email=request.user).wallet
                    if payee.eth_address == DEFAULT_ADDRESS:
                        raise "ADDRESS_ERROR"
                    if payer.balance < gig_obj.tokenvalue:
                        raise 'BALANCE_ERROR'
                except "ADDRESS_ERROR":
                    messages.add_message(request,messages.ERROR,'Payee DOES NOT Have An ETH Address Set Up')
                    return redirect('gigs:view-activity')
                except "BALANCE_ERROR":
                    messages.add_message(request,messages.ERROR,'You DO NOT Have Enough Balance')
                    return redirect('gigs:view-activity')
                except:
                    messages.add_message(request,messages.ERROR,'There was a problem transferring funds')
                    return redirect('gigs:view-activity')
                else:
                    payee.balance += gig_obj.tokenvalue
                    payer.balance -= gig_obj.tokenvalue
                    obj.is_paid = True
                    payee.save()
                    payer.save()
                    obj.save()
                    receiver = CustomUser.objects.get(id=val)
                    body = 'You have been paid {} TOKENS in for: {}'.format(Gig.objects.get(id=gig_id).tokenvalue, gig_obj.title)
                    date_sent = now()
                    new_message = Message.objects.create(sender=request.user,receiver=receiver,body=body,date_sent=date_sent)
        
        messages.add_message(request,messages.SUCCESS,'Approved Participants have been paid!')
        return redirect('gigs:view-activity')

class GigGo(TemplateView):
    template_name = 'gigs/gig_go.html'

    def get(self, request, *args, **kwargs):
        # prevent unauthorized access
        # Only approved users can see this page
        gig = GigLocation.objects.get(gig_id=kwargs['pk'])
        user = request.user
        try:
            var = LikedGig.objects.get(user=user,gig_id=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('gigs:home')
        if var.gigapproval.is_approved == True:
            start_address = '{}, {} {}'.format(request.user.userprofile.address1,
                                                 request.user.userprofile.city,
                                                 request.user.userprofile.zipcode)
            start_address_q = re.sub(r'\s',r'+',start_address)
            destination_address = '{}, {} {}'.format(gig.address1,gig.city,gig.zipcode)
            destination_address_q = re.sub(r'\s',r'+',destination_address)
            google_api_key = settings.GOOGLE_DIRECTIONS_API_KEY
            red_url = 'https://www.google.com/maps/embed/v1/directions?key='+google_api_key+'&origin='+start_address_q+'&destination='+destination_address_q
            return render(request,self.template_name,{'start':start_address,'destination':destination_address,'red_url':red_url})
        else:
            return redirect('gigs:home')

    def post(self, request, *args, **kwargs):
        try:
            approval_obj = LikedGig.objects.get(user=request.user,gig_id=kwargs['pk']).gigapproval
        except ObjectDoesNotExist:
            return redirect('gigs:home')
        if approval_obj.is_approved == True:
            approval_obj.is_checkin_requested = True
            approval_obj.save()
            receiver = CustomUser.objects.get(id=approval_obj.liked.gig.poster.id)
            body = 'You have a checkin request for {}. Please verify and approve.'.format(approval_obj.liked.gig.title)
            date_sent = now()
            new_message = Message.objects.create(sender=request.user,receiver=receiver,body=body,date_sent=date_sent)
            messages.add_message(request,messages.SUCCESS,'A checkin request has been submitted')
            return redirect('gigs:view-activity')

        else:
            return redirect('gigs:home')
