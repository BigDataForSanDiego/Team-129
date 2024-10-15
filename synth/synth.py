
import pandas as pd
import numpy as np
from collections import Counter

MAXLAT = 256
MAXLONG = 256

def gen_medications(max_meds=10, lifespan_mean=25, lifespan_std=10, lifespan_min=5):
    medicine = set(['{:04x}'.format(np.random.randint(0, 0xFFFF)) for _ in range(max_meds)])
    # ensures there are max_meds unique values
    while len(medicine) < max_meds: medicine.add('{:04x}'.format(np.random.randint(0, 0xFFFF)))
    medicine = list(medicine)

    lifespan = np.random.normal(lifespan_mean, lifespan_std, max_meds)
    lifespan = np.round(np.maximum(lifespan, lifespan_min))

    meds_df = pd.DataFrame({
        'Medicine': medicine,
        'Lifespan': lifespan
    })

    return meds_df

def gen_clients(medicine, client_count=100, MAXLAT=MAXLAT, MAXLONG=MAXLONG, MAX_DOSAGE=3):
    latitudes = np.random.randint(0, MAXLAT, client_count)
    longitudes = np.random.randint(0, MAXLONG, client_count)

    cs_df = pd.DataFrame({
        'Client': ['Client {:03d}'.format(i) for i in range(client_count)],
        'Lat': latitudes,
        'Long': longitudes,
        'Medicine': np.random.choice(medicine, client_count),
        'Dosage': np.random.randint(1, MAX_DOSAGE, client_count)
    })
    return cs_df

def gen_pharmacies(pharmacy_count=10, MAXLAT=MAXLAT, MAXLONG=MAXLONG):
    pharmacy_names = [f'pharm{i}' for i in range(pharmacy_count)]

    latitudes = np.random.randint(0, MAXLAT, pharmacy_count)
    longitudes = np.random.randint(0, MAXLONG, pharmacy_count)

    rx_df = pd.DataFrame({
        'Name': pharmacy_names,
        'Lat': latitudes,
        'Long': longitudes
    })
    return rx_df

def assign_pharmacies(cs_df, rx_df):
    # distance between each client and each pharm
    client_coords = cs_df[['Lat', 'Long']].values
    pharm = rx_df[['Lat', 'Long']].values

    distances = np.sqrt(
        (
            (client_coords[:, np.newaxis, :] - pharm[np.newaxis, :, :]) ** 2
        ).sum(axis=2))

    # Assign each customer to the closest pharmacy
    closest_pharmacies = np.argmin(distances, axis=1)
    cs_df['Assigned_Pharmacy'] = closest_pharmacies

    return cs_df

def find_pharmacy_demand(cs_df, rx_df):
    # Sort by assigned pharmacy
    total_cs_df = cs_df[['Assigned_Pharmacy','Medicine','Dosage']].groupby(['Assigned_Pharmacy','Medicine']).sum().reset_index().set_index('Assigned_Pharmacy')
    merged_df = pd.merge(rx_df, total_cs_df, right_index=True, left_index=True, how='left')

    # Assign each pharmacy a list of medications that are required

    # use assigned_pharmacy in cs_df to get the pharmacy name, and then get the medicine
    # turn that into a counter and then into a dataframe into demand
    def calculate_demand(group):
        return Counter({medicine: group.loc[group['Medicine'] == medicine, 'Dosage'].sum() for medicine in group['Medicine'].unique()})

    # Apply the function to group by pharmacy ('Name') and calculate demand
    demand_agg = merged_df.groupby('Name').apply(calculate_demand)

    # Assign the aggregated demand back to the original DataFrame
    pharmacy_df = merged_df.drop_duplicates(subset='Name').set_index('Name')
    pharmacy_df['Demand'] = demand_agg
    pharmacy_df = pharmacy_df.drop(columns=['Medicine', 'Dosage'])

    return pharmacy_df