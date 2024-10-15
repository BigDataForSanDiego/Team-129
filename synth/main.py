from synth import *

def main():

    meds_df = gen_medications(med_count=10)
    cs_df = gen_clients(meds_df['Medicine'], client_count=100)
    rx_df = gen_pharmacies(pharmacy_count=10)
    
    cs_df = assign_pharmacies(cs_df, rx_df)
    rx_df = find_pharmacy_demand(cs_df, rx_df)

    print(cs_df)
    print(rx_df)


if __name__ == "__main__":
    main()