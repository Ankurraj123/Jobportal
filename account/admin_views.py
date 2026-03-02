from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from account.models import User
from jobapp.models import Job, Applicant


def superuser_required(view_func):
    """Decorator: only superusers can access these views."""
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Admin access required.')
            return redirect('jobapp:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@superuser_required
def admin_dashboard(request):
    total_employees = User.objects.filter(role='employee', is_superuser=False).count()
    total_employers = User.objects.filter(role='employer', is_superuser=False).count()
    total_jobs = Job.objects.count()
    total_applications = Applicant.objects.count()
    pending_jobs = Job.objects.filter(is_published=False).count()
    recent_employees = User.objects.filter(role='employee', is_superuser=False).order_by('-date_joined')[:5]
    recent_employers = User.objects.filter(role='employer', is_superuser=False).order_by('-date_joined')[:5]
    recent_jobs = Job.objects.order_by('-timestamp')[:5]

    context = {
        'total_employees': total_employees,
        'total_employers': total_employers,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'pending_jobs': pending_jobs,
        'recent_employees': recent_employees,
        'recent_employers': recent_employers,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@superuser_required
def admin_employees(request):
    q = request.GET.get('q', '')
    employees = User.objects.filter(role='employee', is_superuser=False).order_by('-date_joined')
    if q:
        employees = employees.filter(
            Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    context = {'employees': employees, 'q': q}
    return render(request, 'admin_panel/employees.html', context)


@superuser_required
def admin_employers(request):
    q = request.GET.get('q', '')
    employers = User.objects.filter(role='employer', is_superuser=False).order_by('-date_joined')
    if q:
        employers = employers.filter(
            Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    context = {'employers': employers, 'q': q}
    return render(request, 'admin_panel/employers.html', context)


@superuser_required
def admin_jobs(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    jobs = Job.objects.select_related('user', 'category').order_by('-timestamp')
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(company_name__icontains=q))
    if status == 'pending':
        jobs = jobs.filter(is_published=False)
    elif status == 'active':
        jobs = jobs.filter(is_published=True, is_closed=False)
    elif status == 'closed':
        jobs = jobs.filter(is_closed=True)
    context = {'jobs': jobs, 'q': q, 'status': status}
    return render(request, 'admin_panel/jobs.html', context)


@superuser_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    applications = []
    posted_jobs = []
    if user.role == 'employee':
        applications = Applicant.objects.filter(user=user).select_related('job')
    elif user.role == 'employer':
        posted_jobs = Job.objects.filter(user=user).order_by('-timestamp')
    context = {
        'profile_user': user,
        'applications': applications,
        'posted_jobs': posted_jobs,
    }
    return render(request, 'admin_panel/user_detail.html', context)


@superuser_required
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id, is_superuser=False)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.is_active = request.POST.get('is_active') == 'on'
        user.gender = request.POST.get('gender', user.gender)
        user.bio = request.POST.get('bio', user.bio)
        user.skills = request.POST.get('skills', user.skills)
        user.education = request.POST.get('education', user.education)
        user.experience = request.POST.get('experience', user.experience)
        user.save()
        messages.success(request, f'{user.email} updated successfully.')
        return redirect('admin_panel:user_detail', user_id=user.id)
    return render(request, 'admin_panel/user_edit.html', {'profile_user': user})


@superuser_required
def admin_toggle_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_superuser=False)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'{user.email} {status}.')
    return redirect(request.META.get('HTTP_REFERER', 'admin_panel:dashboard'))


@superuser_required
def admin_job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = Applicant.objects.filter(job=job).select_related('user')
    context = {'job': job, 'applicants': applicants}
    return render(request, 'admin_panel/job_detail.html', context)


@superuser_required
def admin_job_approve(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.is_published = True
    job.save()
    messages.success(request, f'"{job.title}" has been approved and published.')
    return redirect('admin_panel:jobs')


@superuser_required
def admin_job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    title = job.title
    job.delete()
    messages.success(request, f'"{title}" has been deleted.')
    return redirect('admin_panel:jobs')
