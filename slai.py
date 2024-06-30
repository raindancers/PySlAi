import boto3
import json
import math

from athenaQuery import SQLQuery, GetTables
from colours import colours
from tools import Tools

# modify this as required. Its likely that you will just need to change the region part
DATABASE_NAME = 'amazon_security_lake_glue_db_ap_southeast_2'

# this uses a cli based profile. Modify so you have a valid session as required. 
session = boto3.session.Session(profile_name='analyst', region_name='ap-southeast-2')

# define the bedrock client
bedrock = session.client('bedrock-runtime')

# define the tools
tools = Tools()

# the message list keeps state of what has been asked and said.
message_list = []

def converse(message_list):
    system = f"""
    - Always include the the database name '{DATABASE_NAME}' in sql querys
    - Use the get_tables tool to get a list of tables in the database
    - Use the sql_db_query tool to query the database
    - Do not use backtick (`) in the SQL Query. 
    - Don't use table JOIN, unless you absolutely have to.
    - ALWAYS use the GROUP BY clause for columns you want to query.
    - Do not use colon `:` in the SQL Query. It causes this error "Error: (sqlalchemy.exc.InvalidRequestError) A value is required for bind parameter".
    - Avoid using aliases(`as` clause) in the SQL Query.
    - When querying column of `string` type, use single quotes ' in SQL Query for casting to string.
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
            
            print(colours.CLAUDE + f"Claude: You'll need to use the tool: {content_block['toolUse']['name']}")

            match content_block['toolUse']['name']:
                case "sql_db_query":
                    query=SQLQuery(content_block['toolUse']['input']['sql'], content_block['toolUse']['toolUseId'])
                    print(colours.ME + 'Me: Ok Mr Claude, I am sending you what i found using the sql_db_tool....')
                    follow_up_blocks.append(query.follow_up_block)

                case "get_tables":
                    query=GetTables(content_block['toolUse']['input']['sql'], content_block['toolUse']['toolUseId'])
                    print(colours.ME + 'Me: Ok Mr Claude, I am sending you what i found using the get_tables tool....')
                    follow_up_blocks.append(query.follow_up_block)
                
                case _:
                    print(colours.WARNING + "That tool does not exist")
    
    return follow_up_blocks

# ---------------------------------------------------------------------------------
print('\n\n\n')
print(colours.HEADER)
print('************************************************************************************************')
print('************************************************************************************************')
print('**                                                                                            **')
print('**  SecurityLake mets Bedrock | using the converse API and Bedrock anthropic.claude-3-sonnet  **')
print('**                                                                                            **')
print('************************************************************************************************')
print('************************************************************************************************')
print(colours.ENDC)
print('\nInputs and Outputs will be prefaced with Claude: | Me: | You:\n')
print('\tResponses marked as Claude: come from the AI LLM')
print('\tResponses marked as Me: are generated locally in this code')
print('\tInput marked as You: are the only really intellegent thing here')
print('\n\nMe: I will ask Claude some questions to get started, so it can collect some hints about what its looking at. Then you can ask some questions')


# the first question must be to find out what is in the database.
message_list.append({
    "role": "user",
    "content": [
        { 
            "text": f"Hey Claude, what Tables are in the Database named {DATABASE_NAME}?. After discovering the tables, get the schema for each table by running a query like 'SELECT * FROM tablename LIMIT 3'. Include the database name in all querys" 
         } 
    ],
})
print(colours.ME + 'Me:',message_list[0]['content'][0]['text'])

#ask claude the question

while True:

    response_message = converse(message_list)
    message_list.append(response_message)

    # check to see claude suggested using a tool
    follow_up_blocks = check_for_tool_use(response_message['content'])

    

    # If there are any followup blocks, we shoudl send them back to Bedrock
    while len(follow_up_blocks) > 0:

        # send the follow up messages.        
        follow_up_message = {
            "role": "user",
            "content": follow_up_blocks,
        }
        message_list.append(follow_up_message)
        response_message = converse(message_list)

        message_list.append(response_message)


        # check to see claude suggested using a tool
        follow_up_blocks = check_for_tool_use(response_message['content'])


    print(colours.CLAUDE + 'Claude:', response_message['content'][0]['text'])
    #message_list.append(response_message)

    # get user input
    user_input = input(colours.YOU + "\nYou: ")
    message_list.append({
        "role": "user",
        "content": [
            { "text": user_input } 
        ],
    })
    


