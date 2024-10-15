def order(cs_df, rx_df):
    return 1


def action(time, cs_df, rx_df, meds_df, shipment_time=7):
    
    if time % shipment_time == 0:
        ord = order(cs_df, rx_df)
    else:
        return 0
