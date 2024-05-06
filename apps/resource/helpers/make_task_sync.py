from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta


def read_apis_sync(api_conector_1 = None,params_1 = {},endpoint_1 = None ,api_conector_2= None, params_2 = {},endpoint_2 = None):
    print(datetime.now())
    with ThreadPoolExecutor(max_workers=2) as executor:
        first_df = executor.submit(api_conector_1,endpoint_1,params_1).result()
        second_df = executor.submit(api_conector_2,endpoint_2,params_2).result()
    print(datetime.now())
    return  first_df, second_df 