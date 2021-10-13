import click
import boto3
import numpy as np
import time
import pandas as pd



client = boto3.client('athena',region_name = 'us-east-1')


def get_var_char_values(d):
    return [obj['VarCharValue'] if len(obj)!=0 else np.nan for obj in d['Data']]
    
def athena_query(query):
    database = "gdelt"
    athena_result_bucket = "s3://myawsathenagdelt/"
    
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': athena_result_bucket
        }
    )
    
    query_execution_id = response["QueryExecutionId"]
    try:
        location,result = wait_get_result(client,query_execution_id)
        result_df = transform_to_dataframe(result)
        return location,result_df
    except:
        print("No result matches")
    

def wait_get_result(client,query_execution_id):
    wait = True
    ### have to wait until state = Succeeded to retrive result
    if not wait:
        print("check s3 bukcet for result")
        #    return response_query_execution_id['QueryExecutionId']
    else:
        response_get_query_details = client.get_query_execution(
            QueryExecutionId = query_execution_id
        )
        status = 'RUNNING'
        iterations = 600 # 30 mins
    
        while (iterations > 0):
            iterations = iterations - 1
            response_get_query_details = client.get_query_execution(
            QueryExecutionId = query_execution_id
            )
            status = response_get_query_details['QueryExecution']['Status']['State']
            
            if (status == 'FAILED') or (status == 'CANCELLED') :
                print("query failed")
                return False, False
    
            elif status == 'SUCCEEDED':
                location = response_get_query_details['QueryExecution']['ResultConfiguration']['OutputLocation']
    
                ## Function to get output results
                response_query_result = client.get_query_results(
                    QueryExecutionId = query_execution_id
                )
                result_data = response_query_result['ResultSet']
                if len(response_query_result['ResultSet']['Rows']) > 1:
                    header = response_query_result['ResultSet']['Rows'][0]
                    rows = response_query_result['ResultSet']['Rows'][1:]
                    header = [obj['VarCharValue'] for obj in header['Data']]
                    result = [dict(zip(header, get_var_char_values(row))) for row in rows]
                    return location, result
                else:
                    return location, None
                    
        else:
                time.sleep(5)
    
        return False
        
def transform_to_dataframe(result):
    df = pd.DataFrame(columns=list(result[0].keys()),index = np.arange(0,len(result),1))
    for i in range(len(result)):
        df.iloc[i] = pd.Series(result[i])
    return df
    

if  __name__=="__main__":
    query = "SELECT globaleventid, day FROM gdelt.events LIMIT 2"
    location,result = athena_query(query)
    print(location)
    print(result)
    # print(result)
    
