# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

import csv
from django.shortcuts import render
import os
import pandas as pd
from pathlib import Path
import json
import logging

BASE_DIR = Path(__file__).resolve(strict=True).parent




@login_required(login_url="/login/")
def index(request):


    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):

    # 지역 csv
    regionfile = BASE_DIR /'Final_CSV/지역.csv/part-00000-d70adea7-1934-4300-afaa-f8ed7ff2fa29-c000.csv'
    region = pd.read_csv(regionfile)
    region['법정동'] = region['시도명'] + ' ' + region['법정동명']
    ind = []
    for i in range(len(region)):
        if region['시도명'][i] == '세종특별자치시':
            ind.append('세종')
        elif len(region['시도명'][i]) == 4:
            ind.append(region['시도명'][i][0] + region['시도명'][i][2] + ' ' + region['법정동명'][i])
        else:
            ind.append(region['시도명'][i][:2] + ' ' + region['법정동명'][i])
    region['short'] = ind


    # 평균근로소득 csv
    salavgfile = BASE_DIR / "Final_CSV/가구.csv/시도별 평균 근로소득.csv"
    salavg = pd.read_csv(salavgfile)
    salavg_labels = list(salavg['시도명'])
    salavg_data = list(salavg['평균근로소득'])

    # 평균가계소득 csv
    houseavgfile = BASE_DIR / "Final_CSV/부동산.csv/시도별 평균 부동산 거래금액.csv"
    houseavg = pd.read_csv(houseavgfile)
    houseavg_labels = list(houseavg['시도명'])
    houseavg_data = list(houseavg['평균부동산거래금액'])

    # 서울 평균 근로소득 csv
    seoulavgfile = BASE_DIR / "Final_CSV/가구.csv/서울특별시 군구별 평균근로소득.csv"
    seoulavg = pd.read_csv(seoulavgfile)
    seoulavg_labels = list(seoulavg['법정동명'])
    seoulavg_data = list(seoulavg['평균근로소득'])


    # 고등학교 csv
    highfile = BASE_DIR /'Final_CSV/고등학교.csv/part-00000-0b88bc1e-b1ea-4cc2-912c-7229d33fd7b5-c000.csv'
    high = pd.read_csv(highfile)
    high = pd.merge(high, region, left_on='주소', right_on='법정동', how='left')
    h1 = high.groupby('학교종류').sum()
    h2 = high.groupby('시도명').count()
    h1_labels = list(h1.index)
    h1_data = list(h1['서울대합격자수'])
    h2_labels = list(h2.index)
    h2_data = list(h2['고등학교명'])
    h3=high[high['시도명']=='서울특별시']
    h3= h3.groupby('법정동명').sum()
    h3_labels =list(h3.index)
    h3_data=list(h3['서울대합격자수'])


    # 중학교 csv
    middlefile= BASE_DIR /'Final_CSV/중학교.csv/part-00000-3f0c90f1-cb8b-4cf9-9df1-397bad86bfa4-c000.csv'
    middle = pd.read_csv( middlefile )
    middle=pd.merge(middle, region, left_on='주소', right_on='법정동',how='left')
    middle1 = middle.groupby('시도명').sum()
    middle2 = middle.groupby('시도명').count()
    m_labels = list(middle1.index)
    m_data = list(middle1['특목고진학자수'])
    m1_data = list(middle2['중학교명'])
    m3 = middle[middle['시도명'] == '서울특별시']
    m3 = m3.groupby('법정동').sum()
    m3_labels = list(m3.index)
    m3_data = list(m3['특목고진학자수'])

    # 교육청 csv
    officefile= BASE_DIR /'Final_CSV/교육청.csv/part-00000-d7c2b366-2591-45be-a27a-41bf85da0021-c000.csv'
    office = pd.read_csv(officefile)
    office_labels = list(office['시도명'])
    office_data = list(office['예산'])

    # # 학군 csv
    studyfile= BASE_DIR /'Final_CSV/학군.csv/학군_final.csv'
    study_region = pd.read_csv(studyfile)
    s_r=pd.merge(study_region, region, on='법정동코드',how='left')
    s_r1 = s_r.groupby('시도명').sum()
    s_r1_labels = list(s_r1.index)
    s_r1_data = list(s_r1['중학교학업중단자수'])
    s_r2_data = list(s_r1['고등학교학업중단자수'])
    s_r3_data = list(s_r1['중등학령인구'])
    s_r['중등교원1인당학생'] = round(s_r['중등학령인구'] / s_r['중등교원총계'],2)
    s_r2=s_r[s_r['시도명']=='서울특별시']
    s_r4_data = list(s_r2['중등교원1인당학생'])



    # 강사 csv
    teacherfile = BASE_DIR /'Final_CSV/강사.csv/part-00000-a48377cd-fce2-4f46-b528-2c333b27f1ae-c000.csv'
    teacher1file = BASE_DIR / 'Final_CSV/강사.csv/part-00001-a48377cd-fce2-4f46-b528-2c333b27f1ae-c000.csv'
    teacher = pd.read_csv( teacherfile)
    df1 = pd.read_csv(teacher1file)
    teacher = pd.concat([teacher, df1])
    teacher.reset_index(drop=True, inplace=True)
    for i in range(len(teacher)):
        teacher['법정동명'][i] = teacher['법정동명'][i].replace(u'\xa0', u' ')
    for i in range(len(teacher)):
        if teacher['법정동명'][i] == '서울 동대문':
            teacher['법정동명'][i] = '서울 동대문구'
        elif teacher['법정동명'][i] == '서울 서대문':
            teacher['법정동명'][i] = '서울 서대문구'
        elif teacher['법정동명'][i] == '서울 영등포':
            teacher['법정동명'][i] = '서울 영등포구'
        elif teacher['법정동명'][i] == '서울 특별시':
            teacher['법정동명'][i] = '서울 중구'
    teac = pd.merge(teacher, region, left_on='법정동명', right_on='short', how='left')
    teacher=teac.groupby('시도명').count()
    teacher_labels = list(teacher.index)
    teacher_data = list(teacher['학원명'])
    teacher1 = teac[teac['시도명'] == '서울특별시']
    teacher1 = teacher1.groupby('법정동').count()
    teacher1_labels = list(teacher1.index)
    teacher1_data = list(teacher1['학원명'])


    # 학원 csv
    acafile = BASE_DIR / 'Final_CSV/학원.csv/part-00000-be35d6e2-37ed-48f9-9ab4-9cf4520b727d-c000.csv'
    aca1file = BASE_DIR / 'Final_CSV/학원.csv/part-00001-be35d6e2-37ed-48f9-9ab4-9cf4520b727d-c000.csv'
    aca = pd.read_csv(acafile)
    aca1 = pd.read_csv(aca1file)
    aca = pd.concat([aca, aca1])
    aca = pd.merge(aca, region, left_on='법정동명', right_on='법정동', how='left')
    aca1 = aca.groupby('시도명').count()
    aca_labels = list(aca1.index)
    aca_data = list(aca1['학원명'])
    aca3 = aca[aca['시도명'] == '서울특별시']
    aca3 = aca3.groupby('법정동명_y').count()
    aca3_labels = list(aca3.index)
    aca3_data = list(aca3['학원명'])

    #유흥업소 csv
    barfile = BASE_DIR / 'Final_CSV/유흥업소.csv/유흥업소.csv'
    bar = pd.read_csv(barfile)
    bar_labels = bar['시도명']
    bar_data = bar['사업장명']

    #지히철 csv
    subfile=BASE_DIR / 'Final_CSV/지하철.csv/지하철.csv'
    sub = pd.read_csv(subfile)
    sub_labels = list(sub['시도명'])
    sub_data = list(sub['지하철역개수'])
    sub_data2 =list(sub['환승역개수'])



    context = {
        # 고등학교
                'h2_labels': h2_labels, 'h2_data': h2_data,
               'h1_labels': h1_labels, 'h1_data': h1_data,
                'h3_labels':h3_labels, 'h3_data':h3_data,
        # 중학교
                'm_labels': m_labels, 'm_data': m_data, 'm1_data' :m1_data,
                'm3_labels':m3_labels, 'm3_data':m3_data,
        # 교육청
                'office_labels': office_labels, 'office_data': office_data,
        # 학군
                's_r1_labels':s_r1_labels, 's_r1_data':s_r1_data, 's_r2_data':s_r2_data,
               's_r3_data':s_r3_data, 's_r4_data' :s_r4_data,
        # 강사
                'teacher_labels' :teacher_labels,'teacher_data':teacher_data,
                'teacher1_labels':teacher1_labels,'teacher1_data':teacher1_data,
        # 학원
                'aca_labels': aca_labels, 'aca_data':aca_data,
                'aca3_labels':aca3_labels,'aca3_data':aca3_data,
        # 근로
                'salavg_labels' :salavg_labels, 'salavg_data':salavg_data,
        # 서울 평균 근로 소득
               'seoulavg_labels': seoulavg_labels, 'seoulavg_data': seoulavg_data,
        # 가계
                'houseavg_labels':houseavg_labels,'houseavg_data':houseavg_data,
        # 유흥업소
               'bar_labels': bar_labels, 'bar_data': bar_data,
        # 지하철
                'sub_labels': sub_labels, 'sub_data': sub_data, 'sub_data2': sub_data2,
                }


    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

