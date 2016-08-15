from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from .models import User,Org,Signatures,PrivacySetup,Notification,Transaction
from django.views.decorators.csrf import requires_csrf_token
from .forms import OrgRegistration,OrgUserRegisterForm,PersonalUserRegistration,ProUserUpdate,UserUpdate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.urlresolvers import reverse
import json
from django.http import JsonResponse
import hashlib
import pyqrcode,code128,pypng
import PIL
from io import BytesIO
# Create your views here.
def index(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            return HttpResponseRedirect("/profile")
    else:
        return render(request,'index.html')

def personal_register(request):
    form=PersonalUserRegistration(request.POST or None)
    if form.is_valid():

        user=form.save(commit=False)
        name=form.cleaned_data['username']
        email=form.cleaned_data['email']
        phone_no=str(form.cleaned_data['phone'])
        pan_no=str(form.cleaned_data['pan'])
        password=form.cleaned_data['password']
        user.set_password(password)
        code=hashlib.sha1(str(name+email+pan_no+timezone.now()).encode())
        code=code.hexdigest()[:13]
        user.code=code
        user.phone=phone_no
        user.pan=pan_no.upper()
        user.email=email.lower()
        user.created=timezone.now()
        user.is_active=True
        user.save()
        temp=PrivacySetup()
        temp.user=user
        temp.save()
        information=authenticate(email=email.lower(),password=password)
        if information is not None:
            if information.is_active:
                login(request, information)
                context={
                    "Log":information.username,
                }
                return HttpResponseRedirect('/')
    context={
        "form":form,
    }
    return render(request, 'registration.html',context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_user(request, call=0):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login')
    else:
        if request.method == "POST":
            email=request.POST['email']
            password=request.POST['password']
            information=authenticate(email=email.lower(),password=password)
            if information is not None:
                if information.is_active:
                    login(request, information)
                    return HttpResponseRedirect('/profile')
                else:
                    context={
                        "error_message":"Your account is not active at this moment please contact Administrator"
                    }
                    return render(request, 'login.html',context)
            else:
                context={
                    "error_message":"The Email Id and Password pair you entered do not match. Please check and try again"
                }
                return render(request, 'login.html', context)
        if (call==1):
            context={
                "error_message":"To Register as an Organization first you must sign in as a user. In case you do not have an account click below to sign up"
            }
            return render(request, 'login.html',context)
        else:
            return render(request, 'login.html')

def org_register(request):
    if request.user.is_authenticated():
        form=OrgRegistration(request.POST or None)
        if form.is_valid():
            org=form.save(commit=False)
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            email=form.cleaned_data['contact_email']
            phone=str(form.cleaned_data['phone'])
            website=form.cleaned_data['website']
            pan=str(form.cleaned_data['pan'])
            password=str(form.cleaned_data['password'])
            org.password=password
            temp=name.split(" ")
            name=""
            for a in range(0,len(temp)):
                temp[a]=temp[a].capitalize()
                name=name+temp[a]+" "
            name.strip(" ")
            org.name=name
            org.address=address
            org.contact_mail=email
            org.phone=phone
            org.website=website
            org.pan=pan.upper()
            org.created=timezone.now()
            org.is_active=True
            org.admin=request.user.email
            org.save()
            about_user=User.objects.get(email=request.user.email)
            about_user.has_org=True
            about_user.is_admin=True
            about_user.org=org
            about_user.save()
            return HttpResponseRedirect('/')
        context={
            "form":form,
            "Log":request.user.username
        }
        return render(request,'org_registration.html',context)
    else:
        return HttpResponseRedirect('/login/')

def user_profile(request):
    organization=False
    admin=False
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.has_org:
                try:
                    organization=request.user.org
                    if(organization):
                        if(request.user.org.admin==request.user.email):
                            admin=True
                            print("admin is true")
                except:
                    organization=False
                    admin=False
                    this_user=User.objects.get(email=request.user.email)
                    this_user.has_org=False
                    this_user.save()
                    print("admin is False")
            context={
                "Log":request.user.username,
                "user_active":True,
                "is_admin":admin,
                "org":organization,
                "profile_info":"active",
            }
            print(context)

            return render(request,'profile_info.html',context)
        else:
            context={
                "cause":"info",
                "message":"Sorry Your account is not active at this moment. Please contact admin",
                "link":"/logout"
            }
            return render(request, 'iwindow.html', context)
    else:
        return HttpResponseRedirect('/login')

def user_profile_update(request):
    error_message=False
    flag=0
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.has_org:
                admin=False
                try:
                    temp=get_object_or_404(Org, admin=request.user.email)
                    admin=True
                except:
                    admin=False
                if request.method == "POST":
                    email=request.POST['email']
                    phone=request.POST['phone']
                    designation=request.POST['designation']
                    if not (email == request.user.email):
                        temp=User.objects.filter(email=email)
                        if temp.count()>0:
                            flag+=1
                    if not (phone==request.user.phone):
                        temp=User.objects.filter(phone=phone)
                        if temp.count()>0:
                            flag+=2
                    if(flag==0):
                        temp=User.objects.get(pk=request.user.pk)
                        temp.email=email
                        temp.phone=phone
                        temp.designation=designation
                        temp.save()
                        if(admin):
                            try:
                                this=request.user.org.contact_mail
                                org=Org.objects.get(contact_mail=this)
                                org.admin=email
                                org.save()
                            except:
                                temp.has_org=False,
                                temp.is_admin=False,
                                temp.org_id=0
                                temp.save()
                        logout(request)
                        return HttpResponseRedirect('/login')
                    elif(flag==2 or flag==3):
                        context={
                            "error_message":"Sorry Another user with the same Phone Number already exist",
                            "Log":request.user.username,
                            "is_admin":admin,
                            "phone":request.user.phone,
                            "pan":request.user.pan,
                            "email":request.user.email,
                            "designation":request.user.designation,
                            "update_profile":"active"
                        }
                        return render(request, 'profile_edit.html',context)
                    else:
                        context={
                            "error_message":"Sorry Another user with the similar Email Id already exist",
                            "Log":request.user.username,
                            "is_admin":admin,
                            "phone":request.user.phone,
                            "pan":request.user.pan,
                            "email":request.user.email,
                            "designation":request.user.designation,
                            "update_profile":"active",
                        }
                        return render(request, 'profile_edit.html',context)
                context={
                    "Log":request.user.username,
                    "phone":request.user.phone,
                    "pan":request.user.pan,
                    "is_admin":admin,
                    "email":request.user.email,
                    "designation":request.user.designation,
                    "update_profile":"active",
                }
                return render(request, 'profile_edit.html', context)
            else:
                if request.method == "POST":
                    email=request.POST['email']
                    phone=request.POST['phone']
                    #designation=request.POST['designation']
                    if not (email == request.user.email):
                        temp=User.objects.filter(email=email)
                        if temp.count()>0:
                            flag+=1
                    if not (phone==request.user.phone):
                        temp=User.objects.filter(phone=phone)
                        if temp.count()>0:
                            flag+=2
                    if(flag==0):
                        temp=User.objects.get(pk=request.user.pk)
                        temp.email=email
                        temp.phone=phone
                        temp.save()
                        logout(request)
                        return HttpResponseRedirect('/login')
                    elif(flag==2 or flag==3):
                        context={
                            "error_message":"Sorry Another user with the similar Phone Number already exist",
                            "Log":request.user.username,
                            "phone":request.user.phone,
                            "pan":request.user.pan,
                            "email":request.user.email,
                            "update_profile":"active",
                        }
                        return render(request, 'profile_edit.html',context)
                    else:
                        context={
                            "error_message":"Sorry Another user with the similar Email Id already exist",
                            "Log":request.user.username,
                            "phone":request.user.phone,
                            "pan":request.user.pan,
                            "email":request.user.email,
                            "update_profile":"active",
                        }
                        return render(request, 'profile_edit.html',context)
                context={
                    "Log":request.user.username,
                    "phone":request.user.phone,
                    "pan":request.user.pan,
                    "email":request.user.email,
                    "update_profile":"active",
                }
                return render(request, 'profile_edit.html', context)
    else:
        return HttpResponseRedirect("/login")

def user_profile_privacy(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            admin=False
            try:
                org=request.user.org
                if(org.admin==request.user.email):
                    admin=True
            except:
                admin=False
            try:
                temp=get_object_or_404(PrivacySetup,user=request.user)
                context={
                    "Log":request.user.username,
                    "privacy":"active",
                    'has_org':bool(request.user.has_org),
                    "is_admin":admin,
                    'personal_phone':bool(temp.personal_result_phone_number),
                    'professional_phone':bool(temp.professional_result_phone_number),
                    'profile_phone':bool(temp.profile_view_phone_number),
                    'personal_mail':bool(temp.personal_result_email),
                    'professional_mail':bool(temp.professional_result_email),
                    'profile_mail':bool(temp.profile_view_email),
                    'personal_address':bool(temp.personal_result_address),
                    'profile_address':bool(temp.profile_view_address),
                    'personal_gender':bool(temp.personal_result_gender),
                    'profile_gender':bool(temp.profile_view_gender),
                    'profile_dob':bool(temp.show_dob),
                    'user':request.user
                }
            except:
                temp=PrivacySetup()
                temp.user=request.user
                temp.save()
                context={
                    "Log":request.user.username,
                    "privacy":"active",
                    "is_admin":admin,
                    'has_org':bool(request.user.has_org),
                    'personal_phone':bool(temp.personal_result_phone_number),
                    'professional_phone':bool(temp.professional_result_phone_number),
                    'profile_phone':bool(temp.profile_view_phone_number),
                    'personal_mail':bool(temp.personal_result_email),
                    'professional_mail':bool(temp.professional_result_email),
                    'profile_mail':bool(temp.profile_view_email),
                    'personal_address':bool(temp.personal_result_address),
                    'profile_address':bool(temp.profile_view_address),
                    'personal_gender':bool(temp.personal_result_gender),
                    'profile_gender':bool(temp.profile_view_gender),
                    'profile_dob':bool(temp.show_dob),
                    'user':request.user
                }
            return render(request,'profile_privacy.html',context)
    else:
        return HttpResponseRedirect('/login')

def user_profile_settings(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            total=0
            last_purchase=0
            total_signatures=Transaction.objects.filter(user=request.user)
            if (total_signatures.count()>0):
                for sign in total_signatures:
                    total=total+sign.amount
            recent_signature=Transaction.objects.filter(user=request.user).order_by("-date_of_purchase")
            last_purchase=recent_signature[0].amount
            admin=False
            try:
                if(request.user.org.admin==request.user.email):
                    admin=True
            except:
                user=User.objects.get(email=request.user.email)
                user.is_admin=False
                user.org=0
                user.save()
            pro_total_sign=0
            try:
                pro_sign=Signatures.objects.filter(created=request.user.email,org=request.user.org)
                pro_total_sign=pro_sign.count()
            except:
                pro_total_sign=0
            if request.method=='POST':
                action=request.POST['action']
                if(action=="password_update"):
                    new_password=request.POST['content1']
                    old_password=request.POST['content2']
                    this_user=User.objects.get(pk=request.user.pk)
                    information=authenticate(email=this_user.email,password=old_password)
                    if information is not None:
                        this_user.set_password(new_password)
                        this_user.save()
                        return JsonResponse({'response':True})
                    else:
                        return JsonResponse({'response':False})
            context={
                "Log":request.user.username,
                "settings":"active",
                "total_sign":total,
                "last_purchase":last_purchase,
                "is_admin":admin,
                "total_pro_sign":pro_total_sign,
            }
            return render(request,'profile_settings.html',context)
    else:
        return HttpResponseRedirect('/login')


def user_profile_signature_control(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            admin=False
            try:
                org=request.user.org
                if(org.admin==request.user.email):
                    admin=True
            except:
                admin=False
            personal_sign=Signatures.objects.filter(created=request.user.email, org=0).order_by('-date_created')
            for temp in personal_sign:
                temp.url=reverse('winker:search_code',kwargs={'code':temp.code})
                temp.url=request.build_absolute_uri(temp.url)
            context={
                "Log":request.user.username,
                "signature_control":"active",
                "personal_sign":personal_sign,
                "is_admin":admin,
            }
            if request.user.has_org:
                pro_sign=Signatures.objects.filter(created=request.user.email, org=request.user.org).order_by('-date_created')
                for temp in pro_sign:
                    temp.url=reverse('winker:search_code',kwargs={'code':temp.code})
                    temp.url=request.build_absolute_uri(temp.url)
                context={
                    "Log":request.user.username,
                    "signature_control":"active",
                    "personal_sign":personal_sign,
                    "pro":True,
                    "pro_sign":pro_sign,
                    "is_admin":admin,
                }
            return render(request,'profile_signature_control.html',context)
    else:
        return HttpResponseRedirect('/login')

@requires_csrf_token
def user_profile_workspace(request):
    savings=''
    if request.user.is_authenticated():
        if request.user.is_active:
            admin=False
            try:
                org=request.user.org
                if(org.admin==request.user.email):
                    admin=True
            except:
                admin=False
            sign=Signatures.objects.filter(created=request.user.email)
            total_signatures=sign.count()
            if(total_signatures<8333):
                savings=str(total_signatures)+" pages till now. Keep it up!"
            else:
                result=divmod(total_signatures,8333)
                savings=str(result[0])+" trees, but "+str(result[1])+" pages till now. Keep it up!"
            if request.user.has_org:
                context={
                    "Log":request.user.username,
                    "workspace":"active",
                    "savings":savings,
                    "has_org":True,
                    "is_admin":admin,
                }
            else:
                context={
                    "Log":request.user.username,
                    "workspace":"active",
                    "savings":savings,
                    "has_org":False,
                    "is_admin":admin,
                }
            return render(request,'profile_workspace.html',context)
    else:
        return HttpResponseRedirect('/login')

def personal_signature(request):
    if request.method == "POST":
        data=request.body
        letter_head=str(request.POST['letter_head']).upper()
        addressed_to=str(request.POST['addressed_to']).upper()
        subject=str(request.POST['subject'].upper())
        temp=Signatures.objects.filter(header=letter_head,addressed_to=addressed_to,created=request.user.email,subject=subject)
        if temp.count()>0:
            return JsonResponse({'success':False,'reason':1})
        else:
            if(int(request.user.signature_left_per)>0):
                comment=request.POST['comments']
                date_created=timezone.now()
                is_valid=True
                hash_object=hashlib.sha1(str(data).encode())
                code=hash_object.hexdigest()
                create=Signatures()
                create.code=code
                create.date_created=date_created
                create.header=letter_head
                create.created=request.user.email
                create.signatory=str(request.user.email)
                create.is_valid=is_valid
                create.contact=request.user.email
                create.addressed_to=addressed_to
                create.comments=comment
                create.subject=subject
                sign_reduce=User.objects.get(email=request.user.email)
                sign_reduce.signature_left_per-=1
                sign_reduce.save()
                if(sign_reduce.signature_left_per<4):
                    icode=hashlib.sha1(str("PER_LOW_SIGN"+str(timezone.now)+request.user.email).encode())
                    icode=icode.hexdigest()[:15]
                    notify=Notification()
                    notify.type="PER_LOW_SIGN"
                    notify.created_by="system"
                    notify.request_operation="refill"
                    notify.targeted_audience=request.user.email
                    notify.code=icode
                    notify.save()
                if not create.save():
                    temp=reverse('winker:ghost_window',kwargs={'key':code})
                    url=request.build_absolute_uri(temp)
                    return JsonResponse({'success':True, 'code':url})
                else:
                    return JsonResponse({'success':False,'reason':0})
            else:
                return JsonResponse({'success':False,'reason':4})

def professional_signature(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            if request.user.is_active:
                if request.user.is_valid:
                    data=request.body
                    org=''
                    try:
                        org=request.user.org
                    except:
                        return JsonResponse({'success':False, 'reason':4})
                    if org:
                        letter_head=request.POST['letter_head'].upper()
                        addressed_to=request.POST['addressed_to'].upper()
                        subject=request.POST['subject'].upper()
                        comments=request.POST['comments']
                        temp=Signatures.objects.filter(header=letter_head,addressed_to=addressed_to,created=request.user.email,subject=subject,org=request.user.org)
                        if temp.count()>0:
                            return JsonResponse({'success':False,'reason':1})
                        else:
                            if (int(request.user.signature_left_org)>0):
                                hash_code=hashlib.sha1(str(data).encode())
                                code=hash_code.hexdigest()
                                create=Signatures()
                                create.org=org
                                create.date_created=timezone.now()
                                create.header=letter_head
                                create.created=str(request.user.email)
                                create.contact=str("Email: "+request.user.org.contact_mail+", Phone: "+request.user.org.phone)
                                create.signatory=str(request.user.email)
                                create.is_valid=True
                                create.comments=comments
                                create.code=code
                                create.subject=subject
                                create.addressed_to=addressed_to
                                reduce_sign=User.objects.get(email=request.user.email)
                                reduce_sign.signature_left_org-=1
                                reduce_sign.save()
                                if(reduce_sign.signature_left_org<10):
                                    icode=hashlib.sha1(str("SIGN_REFILL_PRO"+str(timezone.now)+request.user.email).encode())
                                    icode=icode.hexdigest()
                                    icode=icode[:15]
                                    notify=Notification()
                                    notify.type="SIGN_REFILL_PRO" #REQUESTING ADMIN TO REFIL SIGNATURES
                                    notify.created_by=request.user.email
                                    notify.targeted_audience="admin"
                                    notify.request_operation="refill"
                                    notify.org_related=request.user.org
                                    notify.code=icode
                                    notify.date_created=timezone.now()
                                    notify.save()
                                if not create.save():
                                    temp=reverse('winker:ghost_window',kwargs={'key':code})
                                    url=request.build_absolute_uri(temp)
                                    return JsonResponse({'success':True,'code':url})
                                else:
                                    return JsonResponse({'success':False,'reason':0})
                            else:
                                return JsonResponse({'success':False,'reason':4})


def code_search(request,code):

    if request.method == 'POST':
        temp=''
        try:
            temp=get_object_or_404(Signatures, code=code)
            record_org=''
            try:
                record_org=temp.org.name
                if not temp.is_valid:
                    return JsonResponse({
                        'record':True,
                        'org':record_org,
                        'code':temp.code,
                        'addressed_to':temp.addressed_to,
                        'is_valid':False,
                        'header':temp.header,
                        'subject':temp.subject,
                        'signatory':temp.signatory,
                        'created_by':temp.created,
                        'record_date':temp.date_created,
                        'invalidated_by':temp.invalidated_by,
                        'invalidated_on':temp.invalidated_on,
                        'invalidated_reason':temp.invalidated_reason
                    })
                else:
                    return JsonResponse({
                        'record':True,
                        'org':record_org,
                        'code':temp.code,
                        'addressed_to':temp.addressed_to,
                        'is_valid':True,
                        'header':temp.header,
                        'subject':temp.subject,
                        'created_by':temp.created,
                        'record_date':temp.date_created,
                        'contact':temp.contact,
                        'signatory':temp.signatory,
                    })
            except:
                if not temp.is_valid:
                    return JsonResponse({
                        'record':True,
                        'code':temp.code,
                        'addressed_to':temp.addressed_to,
                        'is_valid':False,
                        'flag':temp.is_flagged,
                        'flag_reason':temp.flag_reason,
                        'date_of_blog':temp.flagged_on,
                        'header':temp.header,
                        'subject':temp.subject,
                        'signatory':temp.signatory,
                        'created_by':temp.created,
                        'record_date':temp.date_created,
                        'invalidated_by':temp.invalidated_by,
                        'invalidated_on':temp.invalidated_on,
                        'invalidated_reason':temp.invalidated_reason
                    })
                else:
                    return JsonResponse({
                        'record':True,
                        'code':temp.code,
                        'addressed_to':temp.addressed_to,
                        'is_valid':True,
                        'flag':temp.is_flagged,
                        'flag_reason':temp.flag_reason,
                        'date_of_blog':temp.flagged_on,
                        'header':temp.header,
                        'subject':temp.subject,
                        'created_by':temp.created,
                        'record_date':temp.date_created,
                        'contact':temp.contact,
                        'signatory':temp.signatory,
                    })
        except:
            return JsonResponse({'record':False})
    elif request.method == 'GET':
        temp=''
        context={}
        try:
            temp=get_object_or_404(Signatures, code=code)
            record_org=''
            user=User.objects.get(email=temp.created)
            user_privacy=PrivacySetup.objects.get(user=user)
            try:
                record_org=temp.org
                admin=False
                if(record_org.admin==request.user.email):
                    admin=True
                context={
                    'record':True,
                    'org':record_org,
                    'sign':temp,
                    'admin':admin,
                    'signatory':user,
                    'user_privacy':user_privacy,
                }
                if request.user.is_authenticated():
                    context['Log']=request.user.username
                return render(request, 'record_view.html', context)
            except:
                context={
                    'record':True,
                    'sign':temp,
                    'signatory':user,
                    'user_privacy':user_privacy,
                }
                if request.user.is_authenticated():
                    context['Log']=request.user.username
                return render(request, 'record_view.html', context)

        except:
            context={
                'record':False,
            }
            if request.user.is_authenticated():
                context['Log']=request.user.username
            return render(request, 'record_view.html', context)

def image_code_generator(request, key):
    temp=''
    if request.user.is_authenticated():
        try:
            temp=get_object_or_404(Signatures, code=key)
            if(temp.created==request.user.email):
                qr_code=reverse('winker:show_qr_code',kwargs={'code':key})
                qr_code=request.build_absolute_uri(qr_code)
                bar_code=reverse('winker:show_bar_code',kwargs={'code':key})
                bar_code=request.build_absolute_uri(bar_code)
                url=reverse('winker:search_code',kwargs={'code':key})
                url=request.build_absolute_uri(url)
                context={
                    'record':True,
                    'code':key,
                    'url':url,
                    'qr_code':qr_code,
                    'bar_code':bar_code,
                }
                return render(request,'iwindow.html',context)
            else:
                context={
                    'record':False,
                    'error_message':'You are not authorised to see this content',
                }
                return render(request,'iwindow.html',context)
        except:
            context={
                'record':False,
                'error_message':"No such data exists",
            }
            return render(request, 'iwindow.html',context)
    else:
        context={
            'record':False,
            'error_message':'Request forbidden! You knocked into wrong window',
        }
        return render(request,'iwindow.html',context)

@requires_csrf_token
def show_qr_code(request, code):
    if request.method=="GET":
        try:
            temp=get_object_or_404(Signatures,code=code)
            url=reverse('winker:search_code',kwargs={'code':code})
            url=request.build_absolute_uri(url)
            qr=pyqrcode.create(url,mode='binary')
            buffer=BytesIO()
            qr.png(buffer,scale=4)
            buffer.seek(0)
            return HttpResponse(buffer,content_type='image/png')
        except:
            return HttpResponse("No Data")

@requires_csrf_token
def show_bar_code(request, code):
    if request.method=="GET":
        try:
            temp=get_object_or_404(Signatures,code=code)
            url=reverse('winker:search_code',kwargs={'code':code})
            url=request.build_absolute_uri(url)
            buffer=BytesIO()
            code128.image(url,height=100,thickness=2,quiet_zone=True).save(buffer, 'PNG')
            buffer.seek(0)
            return HttpResponse(buffer,content_type='image/png')
        except:
            return HttpResponse("No Data")

@requires_csrf_token
def flag_raiser(request):
    context=''
    if request.method=="POST":
        if request.user.is_authenticated():
            temp=get_object_or_404(Signatures,code=str(request.POST['key']))
            try:
                if temp.created==request.user.email:
                    if not temp.is_valid:
                        context={
                            'report':False,
                            'reason':"Invalidated Document"
                        }
                    else:
                        if temp.is_flagged:
                            temp.is_flagged=False
                            temp.flag_reason="NULL"
                            temp.flagged_by="NULL"
                            temp.save()
                            context={
                                'report':True,
                            }
                        else:
                            temp.is_flagged=True
                            temp.flag_reason=str(request.POST['flag_reason']).upper()
                            temp.flagged_by=request.user.email
                            temp.flagged_on=timezone.now()
                            temp.save()
                            context={
                                'report':True,
                            }
                else:
                    context={
                        'report':False,
                        'reason':"You are not allowed to perform this operation. Contact the creator of this signature for such concern",
                    }
            except:
                context={
                    'report':False,
                    'reason':"No such data exist",
                }
        else:
            context={
                'report':False,
                'reason':"Request forbidden. Unauthorised Request",
            }
    return JsonResponse(context)

def flagwindow(request, key):
    if request.user.is_authenticated():
        if request.method=="GET":
            temp=get_object_or_404(Signatures, code=str(key))
            try:
                if(temp.created==request.user.email or temp.addressed_to==request.user.email):
                    if(temp.is_flagged):
                        context={
                            'status':False,
                            'user':True
                        }
                        return render(request, 'flag_handler.html', context)
                    else:
                        if(temp.is_valid):
                            context={
                                'status':True,
                                'key':key
                            }
                            return render(request, 'flag_handler.html', context)
                        else:
                            context={
                                'status':False,
                                'user':True
                            }
                            return render(request, 'flag_handler.html', context)
                else:
                    context={
                        'status':False,
                        'user':False
                    }
                    return render(request, 'flag_handler.html', context)
            except:
                context={
                    'status':False,
                    'flag':False
                }
                return render(request,'flag_handler.html', context)

@requires_csrf_token
def test_flag(request):
    if request.method=="POST":
        if request.user.is_authenticated():
            key=str(request.POST['key'])
            temp=get_object_or_404(Signatures,code=key)
            try:
                if(temp.created==request.user.email or temp.addressed_to==request.user.email):
                    if not temp.is_valid:
                        return JsonResponse({'status':False,'reason':"Signature invalidated"})
                    else:
                        if temp.is_flagged:
                            if(temp.flagged_by==request.user.email or temp.created==request.user.email):
                                temp.is_flagged=False
                                temp.flagged_by="NULL"
                                temp.flag_reason="NULL"
                                temp.save()
                                return JsonResponse({'status':True,'response':False})
                            else:
                                return JsonResponse({'status':False,'reason':"Un-authorised request"})
                        elif not temp.is_flagged:
                            url=reverse('winker:flag_window',kwargs={'key':key})
                            url=request.build_absolute_uri(url)
                            return JsonResponse({'status':True,'response':url})
                else:
                    return JsonResponse({'status':False,'reason':'Unauthorised Request'})
            except:
                return JsonResponse({'status':False,'reason':"No such record exist"})

@requires_csrf_token
def test_validity(request):
    if request.method=="POST":
        if request.user.is_authenticated():
            key=request.POST['key']
            if(key):
                temp=get_object_or_404(Signatures, code=str(request.POST['key']))
                try:
                    if temp.created==request.user.email:
                        if temp.is_valid:
                            url=reverse('winker:invalidation_page', kwargs={'key':key})
                            url=request.build_absolute_uri(url)
                            context={
                                'status':True,
                                'url':url,
                            }
                            return JsonResponse(context)
                        else:
                            context={
                                'status':False,
                                'reason':'KeyAlreadyInvalid'
                            }
                            return JsonResponse(context)
                    else:
                        context={
                            'status':False,
                            'reason':'UnauthorisedRequest'
                        }
                        return JsonResponse(context)
                except:
                    context={
                        'status':False,
                        'reason':'KeyError'
                    }
                    return JsonResponse(context)

def invalidation_window(request,key):
    if request.method=="GET":
        if request.user.is_authenticated():
            if request.user.is_active:
                temp=get_object_or_404(Signatures, code=key)
                try:
                    if temp.created==request.user.email:
                        if temp.is_valid:
                            context={
                                'status':True,
                                'key':temp.code,
                            }
                            return render(request,'invalidate.html', context)
                        else:
                            context={
                                'status':False,
                                'reason':"SignatureAlreadyInvalid",
                            }
                            return render(request,'invalidate.html',context)
                    else:
                        context={
                            'status':False,
                            'reason':"UnauthorisedRequest",
                        }
                        return render(request,'invalidate.html',context)
                except:
                    context={
                        'status':False,
                        'reason':"KeyError",
                    }
                    return render(request,'invalidate.html',context)
        else:
            context={
                'status':False,
                'reason':'BadRequest'
            }
            return render(request,'invalidate.html',context)


def invalidation_submit(request):
    #print("Gotcha! Key: "+request.POST['key']+" and Reason is: "+request.POST['invalidation_reason'])
    context=''
    if request.method=="POST":
        if request.user.is_authenticated():
            temp=get_object_or_404(Signatures, code=str(request.POST['key']))
            try:
                if temp.created==request.user.email:
                    if temp.is_valid:
                        temp.is_valid=False
                        temp.invalidated_on=timezone.now()
                        temp.invalidated_by=request.user.email
                        temp.invalidated_reason=str(request.POST['invalidation_reason']).upper()
                        temp.save()
                        code=hashlib.sha1(str("INVALIDATE_SIGN"+timezone.now()+request.user.email).encode())
                        code=code.hexdigest()[:15]
                        notify=Notification()
                        notify.type="INVALIDATE_SIGN"
                        notify.code=code
                        notify.date_created=timezone.now()
                        notify.created_by=request.user.email
                        notify.targeted_audience="admin"
                        notify.org_related=request.user.org
                        notify.request_signature=temp.code
                        notify.save()
                        context={
                            'status':True
                        }
                        return JsonResponse(context)
                    else:
                        context={
                            'status':False,
                            'reason':'SignatureAlreadyInvalid'
                        }
                        return JsonResponse(context)
                else:
                    context={
                        'status':False,
                        'reason':"UnauthorisedRequest"
                    }
                    return JsonResponse(context)
            except:
                context={
                    'status':False,
                    'reason':'SignatureKeyError'
                }
                return JsonResponse(context)

def privacy_control(request):
    if request.method=='POST':
        if request.user.is_authenticated():
            if request.user.is_active:
                context=''
                possible=('personal_phone','personal_mail','personal_gender','personal_address','pro_phone','pro_mail','profile_phone','profile_mail','profile_address','profile_gender','profile_dob')
                operation=str(request.POST['operation'])
                if(operation in possible):
                    try:
                        temp=get_object_or_404(PrivacySetup,user=request.user)
                    except:
                        temp=PrivacySetup()
                        temp.user=request.user
                        temp.save()
                    finally:
                        if(operation == 'personal_phone'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.personal_result_phone_number):
                                me.personal_result_phone_number=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.personal_result_phone_number=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'personal_mail'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.personal_result_email):
                                me.personal_result_email=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.personal_result_email=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == "personal_address"):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.personal_result_address):
                                me.personal_result_address=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.personal_result_address=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'personal_gender'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.personal_result_gender):
                                me.personal_result_gender=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.personal_result_gender=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == "pro_phone"):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.professional_result_phone_number):
                                me.professional_result_phone_number=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.professional_result_phone_number=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'pro_mail'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.professional_result_email):
                                me.professional_result_email=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.professional_result_email=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'profile_phone'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.profile_view_phone_number):
                                me.profile_view_phone_number=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.profile_view_phone_number=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'profile_mail'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.profile_view_email):
                                me.profile_view_email=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.profile_view_email=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'profile_address'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.profile_view_address):
                                me.profile_view_address=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.profile_view_address=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'profile_gender'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.profile_view_gender):
                                me.profile_view_gender=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.profile_view_gender=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        if(operation == 'profile_dob'):
                            me=PrivacySetup.objects.get(user=request.user)
                            if(me.show_dob):
                                me.show=False
                                me.save()
                                context={
                                    'report':True,
                                    'status':False
                                }
                            else:
                                me.show_dob=True
                                me.save()
                                context={
                                    'report':True,
                                    'status':True
                                }
                        return JsonResponse(context)
                else:
                    return JsonResponse({'report':False})

def org_admin(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.has_org:
                try:
                    org=request.user.org
                    if(org.admin==request.user.email):
                        context={
                            'Log':request.user.username,
                            'is_admin':True,
                            'has_org':True,
                            'org':org,
                            'notification':0,
                            'org_info':"active",
                        }

                    else:
                        context={
                            'Log':request.user.username,
                            'is_admin':False,
                            'has_org':True,
                            'error_message':"You are not eligible to avail this service",
                        }
                except:
                    temp=User.objects.get(email=request.user.email)
                    temp.has_org=False
                    temp.org_id=0
                    temp.save()
                    context={
                        'Log':request.user.username,
                        'is_admin':False,
                        'has_org':False,
                        'error_message':"Invalid Request",
                    }
                return render(request, 'org_info.html', context)
            else:
                print("no org")
        else:
            print("inactive")
    else:
        return HttpResponseRedirect('/login')

def org_profile_update(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.is_admin:
                try:
                    org=request.user.org
                    if(request.user.org.admin==request.user.email):
                        if request.method=='POST':
                            email=request.POST['email']
                            phone=request.POST['phone']
                            address=request.POST['address']
                            website=request.POST['website']
                            password=request.POST['password']
                            temp=Org.objects.get(admin=request.user.email)
                            output={}
                            error=0
                            if(len(password)>0 and len(password)<8):
                                output['error_message']="Password less then 8 characters are not accepted"
                                error+=1
                            elif(password==temp.password):
                                output['error_message']="Similar Password is not accepted"
                                error+=1
                            else:
                                temp.password=password

                            if(email=="" or email==" "):
                                output['error_message']="Enter a Valid Email Address"
                                error+=1
                            else:
                                temp.contact_mail=email

                            if(len(phone)<10):
                                output['error_message']="Invalid Phone Number"
                                error+=1
                            else:
                                temp.phone=phone

                            if(len(address)==0):
                                output['error_message']="Empty Address in not accepted"
                                error+=1
                            else:
                                temp.address=address

                            if not website:
                                error+=1
                            else:
                                temp.website=website

                            if not error:
                                temp.save()
                                context={
                                    'Log':request.user.username,
                                    'org':temp,
                                    'update_profile':"active",
                                    'success':True,
                                }
                                return render(request,'org_profile_update.html',context)
                            else:
                                context={
                                    "Log":request.user.username,
                                    'org':request.user.org,
                                    'update_profile':"active",
                                    'error':output
                                }
                                print(context)
                                return render(request,'org_profile_update.html', context)
                        context={
                            'Log':request.user.username,
                            'org':org,
                            'update_profile':"active",
                        }
                        return render(request,'org_profile_update.html',context)
                except:
                    temp=User.objects.get(email=request.user.email)
                    temp.is_admin=False
                    temp.has_org=False
                    temp.org_id=0
                    temp.save()
                    return HttpResponseRedirect("/profile")
    else:
        return HttpResponseRedirect('/login')

def org_staff_management(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.is_admin:
                try:
                    temp=request.user.org
                    if(temp.admin==request.user.email):
                        employee=User.objects.filter(org=temp)
                        for this in employee:
                            sign=Signatures.objects.filter(created=this.email,org=temp)
                            total=sign.count()
                            this.total_signature=total
                            if(this.date_org_created=="2015-01-01"):
                                this.date_org_created="N/A"
                        context={
                            'Log':request.user.username,
                            'employee':employee,
                            'org':request.user.org,
                            'staff':"active"
                        }
                        return render(request,'org_employees.html',context)
                    else:
                        this_user=User.objects.get(email=request.user.email)
                        this_user.is_admin=False
                        this_user.save()
                        return HttpResponseRedirect("/profile")
                except:
                    this_user=User.objects.get(email=request.user.email)
                    this_user.is_admin=False
                    this_user.has_org=False
                    this_user.org_id=0
                    this_user.save()
                    return HttpResponseRedirect("/profile")
        else:
            return HttpResponseRedirect("/login")
    else:
        return HttpResponseRedirect("/login")

def org_profile_privacy(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.has_org:
                try:
                    temp=request.user.org
                    if(temp.admin==request.user.email):
                        #place to handle post requests from the view
                        context={
                            'Log':request.user.username,
                            'org':temp,
                            'privacy':"active",
                        }
                        return render(request, 'org_privacy.html',context)
                    else:
                        this_user=User.objects.get(email=request.user.email)
                        this_user.is_admin=False
                        this_user.save()
                        return HttpResponseRedirect("/profile")
                except:
                    this_user=User.objects.get(email=request.user.email)
                    this_user.is_admin=False
                    this_user.has_org=False
                    this_user.org_id=0
                    this_user.save()
                    return HttpResponseRedirect("/profile")
        else:
            return HttpResponseRedirect("/login")
    else:
        return HttpResponseRedirect("/login")

def org_signature_control(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            if request.user.has_org:
                try:
                    org=request.user.org
                    if(org.admin==request.user.email):
                        this=Signatures.objects.filter(org=request.user.org).order_by("-date_created")
                        for a in this:
                            b=User.objects.get(email=a.created)
                            a.created=b.username
                            a.url=reverse('winker:search_code',kwargs={'code':a.code})
                            a.url=request.build_absolute_uri(a.url)
                        if request.method=="POST":
                            key=request.POST['key']
                            action=request.POST['action']
                            if request.user.is_authenticated():
                                if request.user.is_active:
                                    if(org.admin==request.user.email):
                                        try:
                                            trial=get_object_or_404(Signatures,code=key)
                                            if(action=="grant_user_permission"):
                                                trial.hault_user_permission=True
                                                trial.save()
                                                code=hashlib.sha1(str("HAULT"+timezone.now()+request.user.email).encode())
                                                code=code.hexdigest()
                                                code=code[:15]
                                                notify=Notification()
                                                notify.type="HAULT_USE_PERMIT"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="revoke_user_permission"):
                                                trial.hault_user_permission=False
                                                trial.save()
                                                code=hashlib.sha1(str("HAULT"+timezone.now()+request.user.email))
                                                code=code.hexdigest()[:15]
                                                notify=Notification()
                                                notify.type="HAULT_UNUSE_PERMIT"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="hault_grant_user_permission"):
                                                trial.is_haulted=True
                                                trial.hault_user_permission=True
                                                trial.save()
                                                code=hashlib.sha1(str("HAULT"+timezone.now()+request.user.email).encode())
                                                code=code.hexdigest()
                                                code=code[:15]
                                                notify=Notification()
                                                notify.type="HAULT_USE_PERMIT"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="hault_revoke_user_permission"):
                                                trial.is_haulted=True
                                                trial.hault_user_permission=False
                                                trial.save()
                                                code=hashlib.sha1(str("HAULT"+timezone.now()+request.user.email))
                                                code=code.hexdigest()[:15]
                                                notify=Notification()
                                                notify.type="HAULT_UNUSE_PERMIT"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="delete"):
                                                trial.delete()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="unhault"):
                                                trial.is_haulted=False
                                                trial.hault_user_permission=False
                                                trial.save()
                                                code=hashlib.sha1(str("UNHAULT"+timezone.now()+request.user.email))
                                                code=code.hexdigest()[:15]
                                                notify=Notification()
                                                notify.type="UNHAULT"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                            elif(action=="invalidate"):
                                                trial.is_valid=False
                                                trial.invalidated_by=request.user.email
                                                trial.invalidated_on=timezone.now()
                                                trial.invalidated_reason=request.POST['invalidation_reason']
                                                trial.save()
                                                code=hashlib.sha1(str("ORG_INVALIDATE"+timezone.now()+request.user.email))
                                                code=code.hexdigest()[:15]
                                                notify=Notification()
                                                notify.type="ORG_INVALIDATE"
                                                notify.date_created=timezone.now()
                                                notify.created_by=request.user.email
                                                notify.targeted_audience=trial.created
                                                notify.request_signature=trial.code
                                                notify.org_related=request.user.org
                                                notify.code=code
                                                notify.save()
                                                return JsonResponse({'result':True,'action':action,'key':key})
                                        except:
                                            return JsonResponse({'result':False,'error':"InvalidRequest"})
                        context={
                            'Log':request.user.username,
                            'sign':this,
                            'signature_control':"active",
                        }
                        return render(request, 'org_signature_control.html',context)
                except:
                    return HttpResponseRedirect("/profile")
        else:
            return HttpResponseRedirect("/login")
    else:
        return HttpResponseRedirect("/login")

def purchase_window(request,operation):
        if request.user.is_authenticated():
            if request.user.is_active:
                if (operation=="personal"):
                    total=0
                    all_transactions=Transaction.objects.filter(user=request.user)
                    if((all_transactions.count())>0):
                        for transaction in all_transactions:
                            total=total+transaction.amount
                    if request.method=="POST":
                        print("got request")
                        try:
                            this_user=User.objects.get(email=request.user.email)
                            amount=int(request.POST['amount'])
                            this_user.signature_provided_per=int(this_user.signature_left_per)+amount
                            this_user.signature_left_per=int(this_user.signature_left_per)+amount
                            this_user.save()
                            transaction=Transaction()
                            transaction.user=request.user
                            transaction.date_of_purchase=timezone.now()
                            transaction.amount=amount
                            transaction.total_payment=amount*3
                            code=hashlib.sha1(str(str(timezone.now)+str(amount)+str(request.user.email)).encode())
                            code=code.hexdigest()[:15]
                            transaction.code=code
                            transaction.save()
                            print("operation done")
                            return JsonResponse({'response':True})
                        except:
                            return JsonResponse({'response':False})
                    context={
                        'total_transactions':total,
                        'type':'personal',
                    }
                    return render(request,'purchase_window.html',context)
                if(operation=="professional"):
                    if request.user.has_org:
                        try:
                            org=request.user.org
                            if(org.admin==request.user.email):
                                total=0
                                all_transactions=Transaction.objects.get(org=request.user.org)
                                if((all_transactions.count())>0):
                                    for transaction in all_transactions:
                                        total=total+transaction.amount
                                if request.method=="POST":
                                    try:
                                        if(request.user.org.admin==request.user.email):
                                            this_org=Org.objects.filter(org=request.user.org)
                                            try:
                                                amount=request.POST['amount']
                                                this_org.total_signature_purchased=this_org.total_signature_purchased+amount
                                                this_org.latest_signature_purchase=amount
                                                this_org.signatures_left=this_org.signatures_left+amount
                                                this_org.save()
                                                transaction=Transaction()
                                                transaction.org=request.user.org
                                                transaction.date_of_purchase=timezone.now()
                                                transaction.amount=amount
                                                transaction.total_amount=amount*3
                                                code=hashlib.sha1(str(timezone.now()+amount+request.user.org.name).encode())
                                                code=code.hexdigest()[:15]
                                                transaction.code=code
                                                transaction.save()
                                                return JsonResponse({'response':True})
                                            except:
                                                return JsonResponse({'response':False})
                                        else:
                                            return JsonResponse({'response':False})
                                    except:
                                        return JsonResponse({'response':False})
                                context={
                                    'total_transactions':total,
                                    'type':'professional',
                                }
                                return render(request,'purchase_window.html',context)
                        except:
                            return None
