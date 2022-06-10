import pandas as pd
import numpy as np
import time
from datetime import date
import json
import os


def get_all_statuses(old, new):
    new_titles = (new['title'])
    removed = old['title'].isin(new_titles)
    all_changes = pd.merge(old, new, how='outer', on='title')
    
    return all_changes


def create_report(df,roadmap,type):
    
    today = date.today()
    # print("Today's date:", today)
    
    path = f'/Users/nsanchez/Desktop/card_parser/reports/{today}'

    isExist = os.path.exists(path)

    if not isExist:

        os.makedirs(path)
        print("The new directory is created!")

    file_name = f'{roadmap}_report_{type}_{today}'
    file = f'reports/{today}/{file_name}.csv'
    df.to_csv(file, index=False, header=True)

def get_updated_cards(all_changes):
    
    all_changes['changes'] = np.where(all_changes['status_y'].isnull(), "deleted", '')
    all_changes['changes'] = np.where(all_changes['status_x'].isnull(), all_changes['changes'].astype(str) + 'net-new',all_changes['changes'].astype(str) + '' )

    # seperate out updated cards

    updated_cards = all_changes.loc[(all_changes['changes'] == '')]

    updated_cards['desc_c'] = np.where(updated_cards['description_x'] != updated_cards['description_y'], 'description', None )
    updated_cards['stat_c'] = np.where(updated_cards['status_x'] != updated_cards['status_y'], 'status', None )
    updated_cards['cat_c'] = np.where(updated_cards['category_x'] != updated_cards['category_y'], 'category', None )
    updated_cards['date_c'] = np.where(updated_cards['date_x'] != updated_cards['date_y'], 'date', None )
    updated_cards['prod_c'] = np.where(updated_cards['products_x'] != updated_cards['products_y'], 'product(s)', None )
    updated_cards['link_c'] = np.where(updated_cards['link_x'] != updated_cards['link_y'], 'link', None )

    merged = updated_cards[['desc_c', 'stat_c', 'cat_c', 'date_c', 'prod_c', 'link_c']].values.tolist()
    print("******************")
    edit_merged = []
    for item in merged:
        item = set(item)
        if len(item) > 1:
            item.remove(None)
        edit_merged.append(list(set(item)))
        
    print(edit_merged)
    print("******************")
    update_only = all_changes.loc[(all_changes['changes'] == '')]
    update_only['changes'] = edit_merged
    
    return update_only

def get_delete_only(all_changes):

    delete_only = all_changes.loc[(all_changes['changes'] == 'deleted')]
    
    return delete_only

def get_new_only(all_changes):

    new_only = all_changes.loc[(all_changes['changes'] == 'net-new')]
    
    return new_only


def compare_scrape(roadmap_type, old_csv, new_csv):
    
    old = pd.read_csv(old_csv)
    new = pd.read_csv(new_csv)

    # identify net-new, deleted, and updated cards

    all_changes = get_all_statuses(old, new)

    update_only = get_updated_cards(all_changes)

    create_report(update_only,roadmap_type,"update")

    new_only = get_new_only(all_changes)
    
    create_report(new_only,roadmap_type,"new")

    delete_only = get_delete_only(all_changes)
    
    create_report(delete_only,roadmap_type,"delete")


old_cloud_csv = "csv_outputs/cloud_cards_2022-06-08.csv"
new_cloud_csv = "csv_outputs/cloud_cards_2022-06-09.csv"

compare_scrape("cloud", old_cloud_csv, new_cloud_csv)

old_dc_csv = "csv_outputs/dc_cards_2022-06-08.csv"
new_dc_csv = "csv_outputs/dc_cards_2022-06-10.csv"

compare_scrape("dc", old_dc_csv, new_dc_csv)
