import boto3

class Tools():

    def __init__(self):
        self.tool_list = [
            {
                "toolSpec": {
                    "name": "sql_db_query",
                    "description": 'Input to this tool is a detailed and correct SQL query, output is a result from the database.\n    This tool gives access to a real databse.\n    If the query does not return anything or return blank results, it means the query is correct and returned 0 rows.\n    If the query is not correct, an error message will be returned.\n    If an error is returned, re-examine the database using the `sql_db_schema_and_sample_rows` tool, rewrite the query, check the query, and try again.\n    ',
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "sql": {
                                    "type": "string",
                                    "description": "An SQL Statement"
                                }
                            },
                            "required": ["x"]
                        }
                    }
                }
            },
            {
                "toolSpec": {
                    "name": "get_tables",
                    "description": 'Input to this tool is a detailed and correct SQL query, output is a list of tables in the database.\n    This tool gives access to a real databse.\n    If the query does not return anything or return blank results, it means the query is correct and returned 0 rows.\n    If the query is not correct, an error message will be returned.',
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "sql": {
                                    "type": "string",
                                    "description": "An SQL Statement"
                                }
                            },
                            "required": ["x"]
                        }
                    }
                }
            }
        ]
