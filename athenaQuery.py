import boto3
import time
import json

session = boto3.session.Session(profile_name='analyst', region_name='ap-southeast-2')
athena = session.client('athena')

DATABASE_NAME = 'amazon_security_lake_glue_db_ap_southeast_2'
RESULT_OUTPUT_LOCATION = "s3://athenaresultsdoc22/" 

class GetTables():

    def __init__(self, query, tool_use_id):
        self.query = query

        self.follow_up_block = []

        response = athena.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
        )

        has_query_succeeded(response["QueryExecutionId"], 2)

        response = athena.get_query_results(
            QueryExecutionId=response["QueryExecutionId"]
        )

        rows = []
        for row in response['ResultSet']['Rows']:
            rows.append((row['Data'][0]['VarCharValue']))

        self.result = rows

        self.follow_up_block = {
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [
                        {
                            "json": {
                                "result": rows
                            }
                        }
                    ]
                }
            }


class SQLQuery():

    def __init__(self, query):
        self.query = query
        self.result = 'GeneralSQLQuery'

        response = athena.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
        )

        has_query_succeeded(response["QueryExecutionId"], 2)

        response = athena.get_query_results(
            QueryExecutionId=response["QueryExecutionId"]
        )



def has_query_succeeded(execution_id, loop_time):
    state = "RUNNING"
    max_execution = 5

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = athena.get_query_execution(QueryExecutionId=execution_id)
        if (
            "QueryExecution" in response
            and "Status" in response["QueryExecution"]
            and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                return True

        time.sleep(loop_time)

    return False
