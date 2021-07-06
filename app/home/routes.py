# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import gcsfs
import os
import pandas as pd

# CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@blueprint.route('/index')
@login_required
def index():
    # google cloud
    # df = pd.read_csv('gs://test_gocertify_bucket/Main view (Grid).csv')

    # local path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(f'{dir_path}/Main view (Grid).csv')
    unique_brands = df['Brand'].unique()

    brand_dict = []
    for brand in unique_brands:
        df1 = df[df['Brand'] == brand]

        campaigns = len(df1['Campaign'].unique())
        users = len(df1['Email'].unique())
        verification_types = tuple(df1['Verification Type'].unique())
        percent_verified = (len(df1[df1['State'] == 'complete'])/len(df1))*100
        brand_dict.append(
            {
                'brand': brand,
                'campaigns': campaigns,
                'users': users,
                'verification_types': verification_types,
                'percent_verified': percent_verified
            }
        )
    brand_df = pd.DataFrame(brand_dict)

    unique_campaigns = df['Campaign'].unique()
    campaign_dict = []
    for campaign in unique_campaigns:
        df1 = df[df['Campaign'] == campaign]

        brands = len(df1['Brand'].unique())
        users = len(df1['Email'].unique())
        verification_types = tuple(df1['Verification Type'].unique())
        percent_verified = (len(df1[df1['State'] == 'complete']) / len(df1)) * 100
        campaign_dict.append(
            {
                'campaign': campaign,
                'brands': brands,
                'users': users,
                'verification_types': verification_types,
                'percent_verified': percent_verified
            }
        )
    campaign_df = pd.DataFrame(campaign_dict)

    unique_types = df['Verification Type'].unique()
    type_dict = []
    for type_ in unique_types:
        df1 = df[df['Verification Type'] == type_]
        brands = len(df1['Brand'].unique())
        users = len(df1['Email'].unique())
        campaigns = len(df1['Campaign'].unique())
        percent_verified = (len(df1[df1['State'] == 'complete']) / len(df1)) * 100
        type_dict.append(
            {
                'type': type_,
                'campaigns': campaigns,
                'brands': brands,
                'users': users,
                'percent_verified': percent_verified
            }
        )
    type_df = pd.DataFrame(type_dict)
    return render_template('index.html', segment='index', df=df, brand_df=brand_df, campaign_df=campaign_df,
                           type_df=type_df)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
