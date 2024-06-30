# PySlAi
Python Scripts

#### Example Session.

```
************************************************************************************************
************************************************************************************************
**                                                                                            **
**  SecurityLake mets Bedrock | using the converse API and Bedrock anthropic.claude-3-sonnet  **
**                                                                                            **
************************************************************************************************
************************************************************************************************


Inputs and Outputs will be prefaced with one of  Claude: | Me: | You:

        Responses marked as Claude: come from the AI LLM
        Responses marked as Me: are generated locally in this code
        Input marked as You: are the only really intellegent thing here


Me: I will ask Claude some questions to get started, so it can collect some hints about what its looking at. Then you can ask some questions.  You can type exit to quit at the Me: Prompt


Me to Claude: Hey Claude, what Tables are in the Database named amazon_security_lake_glue_db_ap_southeast_2?. After discovering the tables, get the schema for each table by running a query like 'SELECT * FROM tablename LIMIT 3'. Include the database name in all querys
Claude To Me: You'll need to use the tool: get_tables
Me to Claude: Ok Mr Claude, I am sending you what i found using the get_tables tool....
Claude To Me: You'll need to use the tool: sql_db_query

The SQL QUERY to use is:
 SELECT * FROM amazon_security_lake_glue_db_ap_southeast_2.amazon_security_lake_table_ap_southeast_2_cloud_trail_mgmt_2_0 LIMIT 3; 

Me to Claude: Ok Mr Claude, I am sending you what i found using the sql_db_tool....
Claude to You: Got it, the tables in the amazon_security_lake_glue_db_ap_southeast_2 database are:

- amazon_security_lake_table_ap_southeast_2_cloud_trail_mgmt_2_0
- amazon_security_lake_table_ap_southeast_2_route53_2_0  
- amazon_security_lake_table_ap_southeast_2_sh_findings_2_0
- amazon_security_lake_table_ap_southeast_2_vpc_flow_2_0

Let me query each table to get the schema:
Claude To Me: You'll need to use the tool: sql_db_query

The SQL QUERY to use is:
 SELECT * FROM amazon_security_lake_glue_db_ap_southeast_2.amazon_security_lake_table_ap_southeast_2_route53_2_0 LIMIT 3; 

Me to Claude: Ok Mr Claude, I am sending you what i found using the sql_db_tool....
Claude to You: Got it, here are the first few rows and schema for the amazon_security_lake_table_ap_southeast_2_cloud_trail_mgmt_2_0 table:

Columns:
- metadata
- time 
- time_dt
- cloud
- api
- dst_endpoint
- actor
- http_request
- src_endpoint
- session
- policy
- resources
- class_name
- class_uid
- category_name
- category_uid
- severity_id
- severity
- user
- activity_name
- activity_id
- type_uid
- type_name
- status
- is_mfa
- unmapped
- accountid
- region
- asl_version
- observables
Claude To Me: You'll need to use the tool: sql_db_query

The SQL QUERY to use is:
 SELECT * FROM amazon_security_lake_glue_db_ap_southeast_2.amazon_security_lake_table_ap_southeast_2_sh_findings_2_0 LIMIT 3; 

Me to Claude: Ok Mr Claude, I am sending you what i found using the sql_db_tool....
Claude to You: Got it, here are the first few rows and schema for the amazon_security_lake_table_ap_southeast_2_route53_2_0 table:

Columns:
- metadata
- cloud
- src_endpoint
- time
- time_dt  
- query
- answers
- connection_info
- dst_endpoint
- firewall_rule
- severity_id
- severity
- class_name
- class_uid
- category_name
- category_uid
- activity_id
- activity_name
- type_uid
- type_name
- rcode_id
- rcode
- disposition
- action
- action_id
- unmapped
- accountid
- region
- asl_version
- observables
Claude To Me: You'll need to use the tool: sql_db_query

The SQL QUERY to use is:
 SELECT * FROM amazon_security_lake_glue_db_ap_southeast_2.amazon_security_lake_table_ap_southeast_2_vpc_flow_2_0 LIMIT 3; 

Me to Claude: Ok Mr Claude, I am sending you what i found using the sql_db_tool....
Claude to You: Got it, here are the first few rows and schema for the amazon_security_lake_table_ap_southeast_2_sh_findings_2_0 table:

Columns:
- metadata
- time
- time_dt
- confidence_score
- message
- cloud
- resource
- finding_info
- remediation
- compliance
- vulnerabilities
- resources
- evidences
- class_name
- class_uid
- category_name
- category_uid
- severity_id
- severity
- activity_name  
- activity_id
- type_uid
- type_name
- status
- unmapped
- accountid
- region
- asl_version
- observables
Claude to You: Got it, here are the first few rows and schema for the amazon_security_lake_table_ap_southeast_2_vpc_flow_2_0 table:

Columns:
- metadata
- cloud
- src_endpoint
- dst_endpoint
- connection_info
- traffic
- time
- time_dt
- start_time_dt
- end_time_dt
- status_code
- severity_id
- severity
- class_name
- class_uid
- category_name
- category_uid
- activity_name
- activity_id
- action
- action_id  
- disposition
- type_uid
- type_name
- accountid
- region
- asl_version
- unmapped
- observables

The key columns seem to be src_endpoint, dst_endpoint, connection_info, traffic details, time information, and resource identifiers like instance_uid.

This covers the schema overview for the main tables in the amazon_security_lake_glue_db_ap_southeast_2 database based on the LIMIT 3 queries.


You to claude: are there any critical events in security hub that occured today? INclude account information. Limit to 20 rows
Claude To Me: You'll need to use the tool: sql_db_query

The SQL QUERY to use is:
 SELECT metadata, finding_info, resources, accountid, region
FROM amazon_security_lake_glue_db_ap_southeast_2.amazon_security_lake_table_ap_southeast_2_sh_findings_2_0
WHERE severity = 'Critical' 
  AND time_dt >= CURRENT_DATE
LIMIT 20; 

Me to Claude: Ok Mr Claude, I am sending you what i found using the sql_db_tool....
Claude to You: Based on the query, here are the critical events found in the Amazon Security Hub findings table that occurred today, limited to 20 rows:

1. Account 7xxxxxxxxxxx0:
- Finding about security groups allowing unrestricted access to high risk ports (AWS Foundational Security Best Practice EC2.19)

2. Account 9xxxxxxxxxx4:
- Finding about enabling hardware MFA for root user (CIS 1.14)
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)
- Finding about enabling MFA for root user (CIS 1.13)

3. Account 0xxxxxxxxxxx7:
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)
- Finding about enabling hardware MFA for root user (CIS 1.14)
- Finding about enabling MFA for root user (CIS 1.13)

4. Account 3xxxxxxxxxx9:
- Finding about enabling MFA for root user (CIS 1.13)
- Finding about enabling hardware MFA for root user (CIS 1.14)
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)

5. Account 8xxxxxxxxxx5:
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)
- Finding about enabling hardware MFA for root user (CIS 1.14)
- Finding about enabling MFA for root user (CIS 1.13)

6. Account 2xxxxxxxxxx8:
- Finding about enabling MFA for root user (CIS 1.13)
- Finding about enabling hardware MFA for root user (CIS 1.14) 
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)

7. Account 3xxxxxxxxxx2:
- Finding about enabling MFA for root user (CIS 1.13)
- Finding about enabling hardware MFA for root user (CIS 1.14)
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)

8. Account 9xxxxxxxxxxx0:
- Finding about enabling hardware MFA for root user (AWS Foundational Security Best Practice IAM.6)

The critical findings are mostly related to not having MFA or hardware MFA enabled for the root user account across multiple AWS accounts, which violates security best practices. One finding is about unrestricted access to high risk ports in a security group.

You to claude: 
```
