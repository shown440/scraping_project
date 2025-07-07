from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse

from app_scrap.manual_fetch import fetch_cia_data_manually  
from app_scrap.models import DataChange, DataPull, CIAData 






@login_required
def start_data_processing(request):
    # Start data processing (in background if possible)
    # For real production, use Celery instead of threading
    import threading
    thread = threading.Thread(target=fetch_cia_data_manually.fetch_and_process_cia_data)
    thread.daemon = True
    thread.start()
    
    return JsonResponse({'status': 'processing_started'})


@login_required
def change_dashboard(request):
    latest_pull = DataPull.objects.filter(is_processed=True).order_by('-pull_time').first()
    all_changes = DataChange.objects.filter(data_pull=latest_pull) if latest_pull else []
    
    # Pagination setup
    page = request.GET.get('page', 1)
    paginator = Paginator(all_changes, 25)  # Show 25 changes per page
    
    try:
        changes = paginator.page(page)
    except PageNotAnInteger:
        changes = paginator.page(1)
    except EmptyPage:
        changes = paginator.page(paginator.num_pages)

    summary = {
        'added': all_changes.filter(change_type='added').count(),
        'removed': all_changes.filter(change_type='removed').count(),
        'modified': all_changes.filter(change_type='modified').count(),
        'total': all_changes.count(),
        'pull_time': latest_pull.pull_time if latest_pull else None
    }
    
    return render(request, 'app_scrap/dashboard.html', {
        'changes': changes,
        'summary': summary
    })



@login_required
def change_history(request):
    pulls_list = DataPull.objects.filter(is_processed=True).order_by('-pull_time')
    paginator = Paginator(pulls_list, 25)  # Show 25 pulls per page
    page = request.GET.get('page')
    pulls = paginator.get_page(page)
    return render(request, 'app_scrap/history.html', {'pulls': pulls})



@login_required
def pull_detail(request, pull_id):
    data_pull = DataPull.objects.get(id=pull_id)
    changes_list = DataChange.objects.filter(data_pull=data_pull)
    
    # Pagination (20 items per page)
    paginator = Paginator(changes_list, 20)
    page = request.GET.get('page')
    try:
        changes = paginator.page(page)
    except PageNotAnInteger:
        changes = paginator.page(1)
    except EmptyPage:
        changes = paginator.page(paginator.num_pages)
    
    context = {
        'data_pull': data_pull,
        'changes': changes,
        'added_count': changes_list.filter(change_type='added').count(),
        'removed_count': changes_list.filter(change_type='removed').count(),
        'modified_count': changes_list.filter(change_type='modified').count(),
    }
    return render(request, 'app_scrap/pull_detail.html', context)



@login_required
def latest_data_pull_view(request): 
    try:
        latest_pull = DataPull.objects.latest('pull_time')
    except DataPull.DoesNotExist:
        latest_pull = None
    
    cia_data = CIAData.objects.none() 
    if latest_pull:
        cia_data = CIAData.objects.filter(data_pull=latest_pull).order_by('created_at')

    paginator = Paginator(cia_data, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'latest_pull': latest_pull,
        'page_obj': page_obj,
    }
    return render(request, 'app_scrap/cia_data_list.html', context)
