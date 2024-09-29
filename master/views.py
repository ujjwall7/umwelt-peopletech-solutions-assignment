from django.shortcuts import render, HttpResponseRedirect, redirect
from . forms import *
from django.contrib import messages
import csv
import pandas
from .models import *
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from urllib.parse import urlparse, parse_qs
from . task import *


def str_to_bool(value):
    if value.lower() in ('true', '1'):
        return True
    elif value.lower() in ('false', '0'):
        return False
    raise ValidationError(f'Invalid boolean value: {value}')

def csvFileExport(request):
    if request.method=='POST':
        form = EnrolleeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            csv_file = data['csv_file']
            print(f"{csv_file = }")
            df = pandas.read_csv(csv_file)

            print(f"{df = }")
            print(f"{df.iterrows() = }")
            for index, row in df.iterrows():
                print(f"{index}")
                try:
                    if Enrollee.objects.filter(enrollee_id = row['enrollee_id']).exists():
                        enrollee = Enrollee.objects.filter(enrollee_id = row['enrollee_id']).last()

                        enrollee.city = row['city']
                        enrollee.city_development_index = row['city_development_index']
                        enrollee.gender = row.get('gender', enrollee.gender)
                        enrollee.relevent_experience = row['relevent_experience']
                        enrollee.enrolled_university = row['enrolled_university']
                        enrollee.education_level = row['education_level']
                        enrollee.major_discipline = row.get('major_discipline', enrollee.major_discipline)
                        enrollee.experience = row['experience']
                        enrollee.company_size = row.get('company_size', enrollee.company_size)
                        enrollee.company_type = row.get('company_type', enrollee.company_type)
                        enrollee.last_new_job = row.get('last_new_job', enrollee.last_new_job)
                        enrollee.training_hours = row['training_hours']
                        enrollee.target = row['target']
                        enrollee.save()
                    else:
                        enrollee = Enrollee(
                            enrollee_id=row['enrollee_id'],
                            city=row['city'],
                            city_development_index=row['city_development_index'],
                            gender=row.get('gender', None),  # Handle null fields
                            relevent_experience=row['relevent_experience'],
                            enrolled_university=row['enrolled_university'],
                            education_level=row['education_level'],
                            major_discipline=row.get('major_discipline', None),
                            experience=row['experience'],
                            company_size=row.get('company_size', None),
                            company_type=row.get('company_type', None),
                            last_new_job=row.get('last_new_job', None),
                            training_hours=row['training_hours'],
                            target=row['target']
                        )
                        enrollee.save()
                    messages.success(request, "your csv exported successfully please refresh again!")
                except Exception as e:
                    print(f"Error = {e}")
                    pass
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {errors}")
            messages.error(request, "“your csv not valid please check again!.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = EnrolleeForm()

    enrollees   = Enrollee.objects.all()

    # Get filter values from the query params
    get_enrollee_id = request.GET.get('enrollee_id')
    get_city = request.GET.get('city')
    get_city_development_index = request.GET.get('city_development_index') #error
    get_gender = request.GET.get('gender')
    get_relevant_experience = request.GET.get('relevant_experience') #error
    get_enrolled_university = request.GET.get('enrolled_university')
    get_education_level = request.GET.get('education_level')
    get_major_discipline = request.GET.get('major_discipline')
    get_experience = request.GET.get('experience')
    get_company_size = request.GET.get('company_size')
    get_company_type = request.GET.get('company_type')
    get_last_new_job = request.GET.get('last_new_job')
    get_training_hours = request.GET.get('training_hours')
    get_target = request.GET.get('target')

    # Apply filters only if the respective filter exists in the query params
    if get_enrollee_id:
        enrollees = enrollees.filter(enrollee_id__icontains=get_enrollee_id)

    if get_city:
        enrollees = enrollees.filter(city__icontains=get_city)  # icontains for partial matching

    if get_city_development_index:
        enrollees = enrollees.filter(city_development_index__icontains=get_city_development_index)

    if get_gender:
        enrollees = enrollees.filter(gender__icontains=get_gender)

    if get_relevant_experience:
        enrollees = enrollees.filter(relevant_experience__icontains=get_relevant_experience)

    if get_enrolled_university:
        enrollees = enrollees.filter(enrolled_university__icontains=get_enrolled_university)

    if get_education_level:
        enrollees = enrollees.filter(education_level__icontains=get_education_level)

    if get_major_discipline:
        enrollees = enrollees.filter(major_discipline__icontains=get_major_discipline)

    if get_experience:
        enrollees = enrollees.filter(experience__icontains=get_experience)

    if get_company_size:
        enrollees = enrollees.filter(company_size__icontains=get_company_size)

    if get_company_type:
        enrollees = enrollees.filter(company_type__icontains=get_company_type)

    if get_last_new_job:
        enrollees = enrollees.filter(last_new_job__icontains=get_last_new_job)

    if get_training_hours:
        enrollees = enrollees.filter(training_hours=get_training_hours)

    if get_target:
        target_bool = str_to_bool(get_target)
        enrollees = enrollees.filter(target__icontains=target_bool)

    paginator   =   Paginator(enrollees,50)
    page_number =   request.GET.get('page')
    page_obj    =   paginator.get_page(page_number)
    total_page  =   page_obj.paginator.num_pages

    context = {}
    context['form'] = EnrolleeForm()
    context['enrollees'] = page_obj
    context['GENDER_CHOICES'] = Enrollee.GENDER_CHOICES
    context['EXPERIENCE_CHOICES'] = Enrollee.EXPERINCE_CHOICES
    context['ENROLLMENT_CHOICES'] = Enrollee.ENROLLMENT_CHOICES
    context['EDUCATION_LEVEL_CHOICES'] = Enrollee.EDUCATION_LEVEL_CHOICES
    context['MAJOR_DISCIPLINE_CHOICES'] = Enrollee.MAJOR_DISCIPLINE_CHOICES
    context['COMPANY_SIZE_CHOICES'] = Enrollee.COMPANY_SIZE_CHOICES
    context['COMPANY_TYPE_CHOICES'] = Enrollee.COMPANY_TYPE_CHOICES
    context['LAST_NEW_JOB_CHOICES'] = Enrollee.LAST_NEW_JOB_CHOICES
    return render(request, "csv_form.html", context)

def exportDataInExcel(request):
    url = request.META.get('HTTP_REFERER')
    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)

    for key in query_params:
        if len(query_params[key]) == 1:
            query_params[key] = query_params[key][0] 
    print(query_params)
    enrollees_data   = Enrollee.objects.all()

    # Get filter values from the query params
    get_enrollee_id = query_params.get('enrollee_id')
    get_city = query_params.get('city')
    get_city_development_index = query_params.get('city_development_index')
    get_gender = query_params.get('gender')
    get_relevant_experience = query_params.get('relevant_experience')
    get_enrolled_university = query_params.get('enrolled_university')
    get_education_level = query_params.get('education_level')
    get_major_discipline = query_params.get('major_discipline')
    get_experience = query_params.get('experience')
    get_company_size = query_params.get('company_size')
    get_company_type = query_params.get('company_type')
    get_last_new_job = query_params.get('last_new_job')
    get_training_hours = query_params.get('training_hours')
    get_target = query_params.get('target')
    print(f"{get_enrollee_id = }")

    # Apply filters only if the respective filter exists in the query params
    if get_enrollee_id:
        enrollees_data = enrollees_data.filter(enrollee_id__icontains=get_enrollee_id)

    if get_city:
        enrollees_data = enrollees_data.filter(city__icontains=get_city)  # icontains for partial matching

    if get_city_development_index:
        enrollees_data = enrollees_data.filter(city_development_index__icontains=get_city_development_index)

    if get_gender:
        enrollees_data = enrollees_data.filter(gender__icontains=get_gender)

    if get_relevant_experience:
        enrollees_data = enrollees_data.filter(relevant_experience__icontains=get_relevant_experience)

    if get_enrolled_university:
        enrollees_data = enrollees_data.filter(enrolled_university__icontains=get_enrolled_university)

    if get_education_level:
        enrollees_data = enrollees_data.filter(education_level__icontains=get_education_level)

    if get_major_discipline:
        enrollees_data = enrollees_data.filter(major_discipline__icontains=get_major_discipline)

    if get_experience:
        enrollees_data = enrollees_data.filter(experience__icontains=get_experience)

    if get_company_size:
        enrollees_data = enrollees_data.filter(company_size__icontains=get_company_size)

    if get_company_type:
        enrollees_data = enrollees_data.filter(company_type__icontains=get_company_type)

    if get_last_new_job:
        enrollees_data = enrollees_data.filter(last_new_job__icontains=get_last_new_job)

    if get_training_hours:
        enrollees_data = enrollees_data.filter(training_hours=get_training_hours)

    if get_target:
        target_bool = str_to_bool(get_target)
        enrollees_data = Enrollee.objects.filter(target__icontains=target_bool)
    
    enrollee_count = enrollees_data.count()
    print(f"{enrollees_data = }")
    get_enrollee_data = enrollees_data.values('enrollee_id', 'city', 'city_development_index', 'gender',
                                    'relevent_experience', 'enrolled_university', 'education_level',
                                    'major_discipline', 'experience', 'company_size', 'company_type',
                                    'last_new_job', 'training_hours', 'target')

    print(f"{get_enrollee_data = }")
    if enrollee_count < 10000:
        df_export = pandas.DataFrame(list(get_enrollee_data))

        # # Create an Excel response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="filtered_enrollee_data.xlsx"'

        df_export.to_excel(response, index=False, engine='openpyxl')
        return response
    else:
        sendMailTask.delay(list(get_enrollee_data))
        messages.success(request, "“The file will be sent to your email shortly.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








