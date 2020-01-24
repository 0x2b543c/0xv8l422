def network_data_adapter(metrics=[str], assets=[str]):
    result = []
    for asset in assets:
        for metric in metrics:
            result.append(f'{asset}.{metric}') 
    return result 


