import boto3
import json
import math

from athenaQuery import SQLQuery, GetTables
from tools import Tools

# this uses a cli based profile. Modify so you have a valid session as required. 
session = boto3.session.Session(profile_name='analyst', region_name='ap-southeast-2')

# define the bedrock client
bedrock = session.client('bedrock-runtime')

# define the tools
tools = Tools()

# the message list keeps state of what has been asked and said.
message_list = []

def converse(message_list):
    system = """
    - The database name is 'amazon_security_lake_glue_db_ap_southeast_2'
    - Use the get_tables tool to get a list of tables in the database
    - Use the sql_db_query tool to query the database 
    """

    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=message_list,
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0
        },
        toolConfig={
            "tools": tools.tool_list
        },
        system=[
            { "text":system },
        ]
    )

    return response['output']['message']

def check_for_tool_use(content):

    follow_up_blocks = []

    for content_block in content:

        if 'toolUse' in content_block:
            
            print(f"Claude: You'll need to use the tool: {content_block['toolUse']['name']}")

            match content_block['toolUse']['name']:
                case "sql_db_query":
                    query=SQLQuery(content_block['toolUse']['input']['sql'])
                    print(query.result)

                case "get_tables":
                    query=GetTables(content_block['toolUse']['input']['sql'], content_block['toolUse']['toolUseId'])
                    print('Me: Ok Mr Claude, I am sending you what i found using that tool....')
                    follow_up_blocks.append(query.follow_up_block)
                
                case _:
                    print("That tool does not exist")
    
    return follow_up_blocks

# ---------------------------------------------------------------------------------

print('************* Security Lake Mets Bedrock using converse API ***************')
print('\n\nLets automatically ask Claude some questions to get started, so its knows whats to look at\n')


# the first question must be to find out what is in the database.
message_list.append({
    "role": "user",
    "content": [
        { "text": "Hey Claude, what Tables are in the Database named 'amazon_security_lake_glue_db_ap_southeast_2'?" } 
    ],
})
print('Me:',message_list[0]['content'][0]['text'])

#ask claude the question
response_message = converse(message_list)
message_list.append(response_message)

# check to see claude suggested using a tool
follow_up_blocks = check_for_tool_use(response_message['content'])


# If there are any followup blocks, we shoudl send them back to Bedrock

if len(follow_up_blocks) > 0:
    
    follow_up_message = {
        "role": "user",
        "content": follow_up_blocks,
    }

    message_list.append(follow_up_message)
    response_message = converse(message_list)

    print('Claude:', response_message['content'][0]['text'])

    message_list.append(response_message)
