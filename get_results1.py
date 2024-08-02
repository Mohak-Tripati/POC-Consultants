# from chain_of_thought import ChainOfThoughtRAG, set_llm
# import dspy
# import sqlite3
# import pandas as pd

# import json
# import os
# import sqlite3
# from dataclasses import asdict, dataclass
# from datetime import datetime, timezone
# from pathlib import Path
# from textwrap import dedent
# from typing import Any, Dict, List, Tuple, Union
# import pandas as pd
# from sqlalchemy import create_engine


# # import pandas as pd

# lm = set_llm()
# dspy.settings.configure(lm=lm)

# class GetResults:
#     def __init__(self, label):
#         self.label = label
    

#     def execute_sql(self,sql_query: str) -> pd.DataFrame:
#         return pd.read_sql_query(sql_query, engine)
    
#     def get_results(self, input_text):
#         if self.label == "tasks":
#             context = """table name: tasks
#             Column name Status : ['To Do', 'In Progress', 'Terminated/Cancelled', 'Development',
#             'Development Complete', 'Done', 'Ready for QC', 'Discovery Phase',
#             'QA level 1 Completed', 'QC Passed', 'QA Completed', 'Hold',
#             'QA level 2 in progress']
#             Other column name are: ['Task ID', 'Task Name', 'Owner', 'Priority', 'Start Date', 'Due Date',
#             'Created Time', 'Status', 'Is Overdue', 'Completion Percentage',
#             'Project Name', 'Milestone Name', 'Project ID', 'Milestone ID',
#             'Parent Task ID', 'Created By ID', 'Owner IDs', 'Task Delay Time',
#             'Task Completion Mode', 'Actual Time Taken', 'Time Spent So Far',
#             'Duration_1', 'Duration Unit', 'Rate Per Hour', 'Clarity Level',
#             'QC Owner']
#             """
#             df = pd.read_excel(r"C:\Users\rabhishek1\Downloads\demo\demo\POC_X\Tasks 1.xlsx")
#         elif self.label == 'milestones':
#             context = """table name: milestones
#             Column name Milestone Status  : ['Upcoming', 'Overdue', 'Completed']
#             Other column names: ['Project Name', 'Milestone Name', 'Owner Name', 'Start Date',
#             'End Date', 'Milestone Status', 'Milestone ID', 'Owner ID',
#             'Project ID', 'Created Time', 'Duration', 'Actual Time Taken',
#             'Milestone Completion Mode', 'Milestone ID String',
#             'Project ID String']
#             """
#             df = pd.read_excel(r"C:\Users\rabhishek1\Downloads\demo\demo\POC_X\Milestones 1.xlsx")
        
#         if os.path.exists(f"C:/Users/HP/Downloads/main code/{self.label}.db"):
#             os.remove(f"C:/Users/HP/Downloads/main code/{self.label}.db")
#             connection = sqlite3.connect(f"{self.label}.db")
#             df.to_sql(name=f"{self.label}", con=connection)
#         engine = create_engine(f'sqlite:///{self.label}.db') 
#         cot=ChainOfThoughtRAG(1, table_context=context)
#         answer=cot(input_text).answer
#         print(answer)
#         if type(answer)=="list":
#             answer = answer[0]
#         def execute_sql(sql_query: str) -> pd.DataFrame:
#             return pd.read_sql_query(sql_query, engine)
#         final_answer=execute_sql(answer)
#         print(final_answer)
#         final_answer = final_answer.to_json()
#         return final_answer
    
# if __name__ == "__main__":
#     gr = GetResults("tasks")
#     print(gr.get_results(input_text="give me records where task delay is more than 30"))

import re
from chain_of_thought import ChainOfThoughtRAG, set_llm, ChainOfThoughtSQLCorrect
import dspy
import sqlite3
import pandas as pd
import json
import os
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql, errors
from dotenv import load_dotenv

# dotenv
load_dotenv()

# Setting up the language model
lm = set_llm()
dspy.settings.configure(lm=lm)

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB = os.getenv('DATABASE_DB')
PORT = os.getenv('PORT')
# DATABASE_USERNAME = "postgres"
# DATABASE_PASSWORD = "valign#123"
# DATABASE_DB = "python_test_poc"
# PORT = 5432


try: 
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=DATABASE_DB,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=PORT
    )

    # Create a cursor object
    cur = conn.cursor()

    # Function to fetch data using SQL query
    def fetch_data(query):
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return columns, rows
    
except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error: {error}")
    # Rollback in case of error
    conn.rollback()
    if conn:
        conn.close()
finally:
    pass

# QueryDatabase class definition
# class QueryDatabase: # ! db starts here
#     def __init__(self, db_path):
#         self.db_path = db_path

#     def execute_sql(self, sql_query: str) -> pd.DataFrame:
#         try:
#             # Connect to the SQLite database
#             # with sqlite3.connect(self.db_path) as connection:
#             #     # Execute the SQL query
#             #     df = pd.read_sql_query(sql_query, connection)
#             # return df
#             # Database connection details
            
#         except Exception as e:
#             print(f"An error occurred while executing the SQL query or error with the DB please check the Query output: {e}")
#             return pd.DataFrame()

# GetResults class definition
class GetResults:
    def __init__(self, label):
        self.label = label
        # self.db_path = os.path.join(os.getcwd(), f"{self.label}.db")
        # self.query_db = QueryDatabase(self.db_path) # ! db execute
    
    
    def get_results(self, input_text):
        # if self.label == "postgres":
        context = """
        Column name status : ['To Do', 'In Progress', 'Terminated/Cancelled', 'Development',
        'Development Complete', 'Done', 'Ready for QC', 'Discovery Phase',
        'QA level 1 Completed', 'QC Passed', 'QA Completed', 'Hold',
        'QA level 2 in progress', 'Closed', 'Requirement Gathering', 'UAT', 'UAT Changes', 'Bug Fix', 'Go Live', 'Training', 'Cancelled', 'Change Request', 'Blocked', 'Data Migration', 'Payment Due']
        ## Database Schema Context

            ### Table: users
            - **Column: user_id**
            - Type: integer
            - Description: Unique identifier for the user. Auto-incremented.
            - **Column: user_name**
            - Type: character varying(255)
            - Description: Name of the user. Must be unique.
            - **Column: user_email**
            - Type: character varying(255)
            - Description: Email address of the user.
            - **Column: role**
            - Type: character varying(50)
            - Description: Role of the user (e.g., Admin, User).
            - **Column: profile**
            - Type: character varying(50)
            - Description: Profile type or description.
            - **Column: status**
            - Type: character varying(50)
            - Description: Status of the user (e.g., Active, Inactive).

            ### Table: projects
            - **Column: project_id**
            - Type: character varying(255)
            - Description: Unique identifier for the project. Auto-incremented.
            - **Column: project_name**
            - Type: character varying(255)
            - Description: Name of the project.
            - **Column: owner**
            - Type: character varying(255)
            - Description: Owner or lead for the project.
            - **Column: start_date**
            - Type: date
            - Description: Date when the project started.
            - **Column: end_date**
            - Type: date
            - Description: Date when the project is expected to end.
            - **Column: status**
            - Type: character varying(50)
            - Description: Current status of the project (e.g., In Progress, Completed).
            - **Column: delivery_team**
            - Type: character varying(255)
            - Description: Team responsible for delivering the project.
            - **Column: project_efforts**
            - Type: integer
            - Description: Estimated effort required for the project (e.g., in hours).
            - **Column: created_time**
            - Type: date
            - Description: Date when the project record was created.

            ### Table: milestones
            - **Column: project_name**
            - Type: character varying(255)
            - Description: Name of the project to which the milestone belongs.
            - **Column: milestone_name**
            - Type: character varying(255)
            - Description: Name of the milestone.
            - **Column: owner_name**
            - Type: character varying(255)
            - Description: Owner or lead for the milestone.
            - **Column: start_date**
            - Type: date
            - Description: Start date of the milestone.
            - **Column: end_date**
            - Type: date
            - Description: End date of the milestone.
            - **Column: milestone_status**
            - Type: character varying(50)
            - Description: Status of the milestone (e.g., Not Started, Completed).
            - **Column: milestone_id**
            - Type: character varying(255)
            - Description: Unique identifier for the milestone.
            - **Column: project_id**
            - Type: character varying(255)
            - Description: Unique identifier for the project to which the milestone belongs.
            - **Column: created_time**
            - Type: date
            - Description: Date when the milestone record was created.
            - **Column: duration**
            - Type: integer
            - Description: Duration of the milestone (e.g., in days).
            - **Column: actual_time_taken**
            - Type: integer
            - Description: Actual time taken to complete the milestone (e.g., in hours).
            - **Column: milestone_completion_mode**
            - Type: character varying(50)
            - Description: Mode of completion for the milestone.
            - **Column: budget**
            - Type: numeric(10,2)
            - Description: Budget allocated for the milestone.
            - **Column: milestone_end_lag**
            - Type: integer
            - Description: Lag in milestone completion.
            - **Column: status**
            - Type: character varying(50)
            - Description: Current status of the milestone.
            - **Column: milestone_value**
            - Type: numeric(10,2)
            - Description: Value associated with the milestone.
            - **Column: application**
            - Type: character varying(255)
            - Description: Application or system related to the milestone.

            ### Table: tasks
            - **Column: task_id**
            - Type: character varying(255)
            - Description: Unique identifier for the task.
            - **Column: task_name**
            - Type: character varying(1024)
            - Description: Name of the task.
            - **Column: owner**
            - Type: character varying(255)
            - Description: Person or team responsible for the task.
            - **Column: priority**
            - Type: character varying(50)
            - Description: Priority level of the task (e.g., High, Medium, Low).
            - **Column: start_date**
            - Type: date
            - Description: Date when the task started.
            - **Column: due_date**
            - Type: date
            - Description: Date by which the task is expected to be completed.
            - **Column: created_time**
            - Type: date
            - Description: Date when the task was created.
            - **Column: duration**
            - Type: integer
            - Description: Expected duration of the task (e.g., in hours).
            - **Column: status**
            - Type: character varying(50)
            - Description: Current status of the task (e.g., To Do, In Progress, Done).
            - **Column: is_overdue**
            - Type: boolean
            - Description: Indicates whether the task is overdue.
            - **Column: completion_percentage**
            - Type: character varying(15)
            - Description: Percentage of completion of the task.
            - **Column: project_name**
            - Type: character varying(255)
            - Description: Name of the project to which the task belongs.
            - **Column: milestone_name**
            - Type: character varying(255)
            - Description: Name of the milestone to which the task belongs.
            - **Column: project_id**
            - Type: character varying(255)
            - Description: Unique identifier for the project.
            - **Column: milestone_id**
            - Type: character varying(255)
            - Description: Unique identifier for the milestone.
            - **Column: task_delay_time**
            - Type: integer
            - Description: Time delay of the task (e.g., in hours).
            - **Column: task_completion_mode**
            - Type: character varying(50)
            - Description: Mode of completion for the task.
            - **Column: actual_time_taken**
            - Type: integer
            - Description: Actual time taken to complete the task (e.g., in hours).
            - **Column: time_spent_so_far**
            - Type: integer
            - Description: Time spent on the task so far (e.g., in hours).
            - **Column: duration_1**
            - Type: numeric
            - Description: Additional duration information (e.g., in hours).
            - **Column: duration_unit**
            - Type: character varying(50)
            - Description: Unit of the duration (e.g., Hours, Days).
            - **Column: clarity_level**
            - Type: character varying(50)
            - Description: Clarity level of the task description.
            - **Column: sprint**
            - Type: character varying(255)
            - Description: Sprint during which the task is being worked on.
            - **Column: billing_type**
            - Type: character varying(50)
            - Description: Type of billing applicable to the task.
            - **Column: product_skill**
            - Type: character varying(255)
            - Description: Skill required for the task related to the product.
            - **Column: sprint_ff_sf**
            - Type: character varying(255)
            - Description: Sprint feature/functionality details.
            - **Column: open_closed**
            - Type: character varying(50)
            - Description: Status of whether the task is open or closed.
            - **Column: allocated_unallocated**
            - Type: character varying(50)
            - Description: Indicates if the task is allocated or unallocated.
            - **Column: days_completed_on**
            - Type: character varying(50)
            - Description: Date when the task was completed.
            - **Column: sprint_new**
            - Type: character varying(255)
            - Description: Details about the new sprint.
            - **Column: completion_date**
            - Type: date
            - Description: Actual date when the task was completed.
            - **Column: qc_owner**
            - Type: character varying(255)
            - Description: Person responsible for quality control of the task.
        """
            # Other column names: [
            #         'task_id', 'task_name', 'owner', 'priority', 'start_date', 'due_date',
            #         'created_time', 'duration', 'status', 'is_overdue', 'completion_percentage',
            #         'project_name', 'milestone_name', 'project_id', 'milestone_id',
            #         'task_delay_time', 'task_completion_mode', 'actual_time_taken', 'time_spent_so_far',
            #         'duration_1', 'duration_unit', 'clarity_level', 'sprint', 'billing_type',
            #         'product_skill', 'sprint_ff_sf', 'open_closed', 'allocated_unallocated',
            #         'days_completed_on', 'sprint_new', 'completion_date', 'qc_owner'
            #     ]
            # ! prev context
            # context = """table name: tasks
            # Column name Status : ['To Do', 'In Progress', 'Terminated/Cancelled', 'Development',
            # 'Development Complete', 'Done', 'Ready for QC', 'Discovery Phase',
            # 'QA level 1 Completed', 'QC Passed', 'QA Completed', 'Hold',
            # 'QA level 2 in progress']
            # Other column names: ['Task ID', 'Task Name', 'Owner', 'Priority', 'Start Date', 'Due Date',
            # 'Created Time', 'Status', 'Is Overdue', 'Completion Percentage',
            # 'Project Name', 'Milestone Name', 'Project ID', 'Milestone ID',
            # 'Parent Task ID', 'Created By ID', 'Owner IDs', 'Task Delay Time',
            # 'Task Completion Mode', 'Actual Time Taken', 'Time Spent So Far',
            # 'Duration_1', 'Duration Unit', 'Rate Per Hour', 'Clarity Level',
            # 'QC Owner']
            # """
             # ! prev context
        # elif self.label == 'milestones':
        #     context = """table name: milestones
        #     Column name Milestone Status  : ['Upcoming', 'Overdue', 'Completed']
        #     Other column names: ['Project Name', 'Milestone Name', 'Owner Name', 'Start Date',
        #     'End Date', 'Milestone Status', 'Milestone ID', 'Owner ID',
        #     'Project ID', 'Created Time', 'Duration', 'Actual Time Taken',
        #     'Milestone Completion Mode', 'Milestone ID String',
        #     'Project ID String']
        #     """

        cot = ChainOfThoughtRAG(1, table_context=context)
        sql_fix = ChainOfThoughtSQLCorrect(1, table_context=context)
        answer = cot(input_text).answer
        print(f"Given answer {answer}")
        answer = sql_fix(answer).answer
        print(f"SQL Corrected Given answer {answer}")
        
        if isinstance(answer, list):
            answer = answer[0]
        
        answer = answer.replace('`','').replace('sql', '')
        print(f"Final answer {answer}")

        # final_answer = self.query_db.execute_sql(answer) # ! final answer is coming from here
            # Fetch completed tasks data
        # completed_tasks_columns, completed_tasks_rows = fetch_data(conn, answer)
        
        completed_tasks_columns, completed_tasks_rows = fetch_data(answer) # ! final answer is coming from here
        # print(completed_tasks_columns, completed_tasks_rows)
            
        # Convert fetched data to DataFrames
        # df_schema_data = {table: pd.DataFrame(rows, columns=columns) for table, (columns, rows) in schema_data.items()}
        df_completed_tasks = pd.DataFrame(completed_tasks_rows, columns=completed_tasks_columns)

        # Convert DataFrames to JSON objects
        # json_schema_data = {table: df.to_json(orient='records') for table, df in df_schema_data.items()}
        json_completed_tasks = df_completed_tasks.to_json(orient='records')
        
        # * database closed
        # cur.close()
        # conn.close()
        
        # print(json_completed_tasks)
        # final_answer = final_answer # ! json is being build here
        # final_answer_dict = {"data": final_answer}
        # final_answer_json = json.dumps(final_answer_dict)
        return json_completed_tasks
        

if __name__ == "__main__":

    gr = GetResults("milestones")
    print(gr.get_results(input_text="give me records where milestone status is 'Completed'"))

