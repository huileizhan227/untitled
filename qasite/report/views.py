from django.shortcuts import render
from django.http import HttpResponse

from .models import TestReport

class ReportType:
    AUTOMATION = 0
    PERFORMANCE = 1
    MONKEY = 2

def index(request):
    rows = TestReport.objects.values('project_name')
    project_name_list = list(set(x['project_name'] for x in rows))
    context = {'project_name_list': project_name_list}
    return render(request, 'report/index.html', context=context)

def project(request, project_name):
    reports = TestReport.objects.filter(
        project_name=project_name
    ).order_by('-build_id')
    context={
        'project_name': project_name,
        'reports': reports
    }
    return render(request, 'report/project.html', context=context)

def detail(request, project_name, build_id):
    test_report = TestReport.objects.get(
        project_name=project_name, build_id=build_id
    )
    context = {'report': test_report}
    if test_report.monkey_report:
        with open(test_report.monkey_report.path) as f:
            text_content = f.read()
        context['monkey_content'] = text_content
    return render(request, 'report/detail.html', context=context)

def latest(request, project_name):
    test_report = TestReport.objects.filter(
        project_name=project_name
    ).order_by('-monkey_report')[0]

    context={
        'report': test_report,
    }
    if test_report.monkey_report:
        with open(test_report.monkey_report.path) as f:
            text_content = f.read()
        context['monkey_content'] = text_content
    return render(request, 'report/detail.html', context=context)


def upload(request):
    report_file = request.FILES['file']
    report_type = int(request.POST['report_type'])
    project_name = request.POST['project_name']
    build_id = request.POST['build_id']
    reports = TestReport.objects.filter(build_id=build_id, project_name=project_name)
    if(len(reports) > 0):
        test_report = reports[0]
    else:
        test_report = TestReport(build_id=build_id, project_name=project_name)
    if report_type == ReportType.AUTOMATION:
        test_report.automated_testing_report = report_file
    elif report_type == ReportType.PERFORMANCE:
        test_report.performance_report = report_file
    elif report_type == ReportType.MONKEY:
        test_report.monkey_report = report_file
    test_report.save()
    return HttpResponse('upload success')
