from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from account.forms import *
from jobapp.permission import user_is_employee 


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')



def employee_registration(request):

    """
    Handle Employee Registration

    """
    form = EmployeeRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/employee-registration.html',context)


def employer_registration(request):

    """
    Handle Employee Registration 

    """

    form = EmployerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('account:login')
    context={
        
            'form':form
        }

    return render(request,'account/employer-registration.html',context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def employee_edit_profile(request, id=id):
    """
    Handle Employee Profile Update Functionality.
    If a new CV (PDF) is uploaded, automatically parse and populate profile fields.
    """
    user = get_object_or_404(User, id=id)
    form = EmployeeProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        user = form.save()
        # Auto-parse CV if a new file was uploaded
        if request.FILES.get('resume'):
            try:
                from account.cv_parser import parse_cv
                data = parse_cv(user.resume.path)
                if 'error' not in data:
                    if data.get('skills'):
                        user.skills = data['skills']
                    if data.get('education'):
                        user.education = data['education']
                    if data.get('experience'):
                        user.experience = data['experience']
                    user.cv_projects     = data.get('cv_projects', [])
                    user.cv_certificates = data.get('cv_certificates', [])
                    user.cv_training     = data.get('cv_training', [])
                    user.cv_achievements = data.get('cv_achievements', [])
                    user.cv_links        = data.get('cv_links', {})
                    user.save()
                    messages.success(request, '✅ Profile updated & CV data extracted successfully!')
                else:
                    messages.warning(request, f'Profile saved but CV parsing failed: {data["error"]}')
            except Exception as e:
                messages.warning(request, f'Profile saved but CV parsing error: {e}')
        else:
            messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={'id': user.id}))
    context = {
        'form': form,
        'profile_user': user,
    }
    return render(request, 'account/employee-edit-profile.html', context)




def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'account/login.html',context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')


@login_required(login_url='/login/')
def user_profile(request):
    """
    Show the logged-in user's full profile.
    """
    from jobapp.models import Job, Applicant
    user = request.user
    context = {'profile_user': user}
    if user.role == 'employee':
        context['applications'] = Applicant.objects.filter(user=user).select_related('job').order_by('-timestamp')
        # Skills list for tag display
        if user.skills:
            context['skills_list'] = [s.strip() for s in user.skills.split(',') if s.strip()]
        else:
            context['skills_list'] = []
        # Pass all structured CV sections
        context['cv_projects']     = user.cv_projects     or []
        context['cv_certificates'] = user.cv_certificates or []
        context['cv_training']     = user.cv_training     or []
        context['cv_achievements'] = user.cv_achievements or []
        context['cv_links']        = user.cv_links        or {}
    elif user.role == 'employer':
        from django.db.models import Count
        posted_jobs = Job.objects.filter(user=user).annotate(
            applicant_count=Count('applicant')
        ).order_by('-timestamp')
        context['posted_jobs'] = posted_jobs
    return render(request, 'account/profile.html', context)