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

from chain_of_thought import ChainOfThoughtRAG, set_llm
import dspy
import sqlite3
import pandas as pd
import json
import os
from sqlalchemy import create_engine

# Setting up the language model
lm = set_llm()
dspy.settings.configure(lm=lm)

# QueryDatabase class definition
class QueryDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_sql(self, sql_query: str) -> pd.DataFrame:
        try:
            # Connect to the SQLite database
            with sqlite3.connect(self.db_path) as connection:
                # Execute the SQL query
                df = pd.read_sql_query(sql_query, connection)
            return df
        except Exception as e:
            print(f"An error occurred while executing the SQL query or error with the DB please check the Query output: {e}")
            return pd.DataFrame()

# GetResults class definition
class GetResults:
    def __init__(self, label):
        self.label = label
        self.db_path = os.path.join(os.getcwd(), f"{self.label}.db")
        self.query_db = QueryDatabase(self.db_path)
    
    def get_results(self, input_text):
        if self.label == "tasks":
            context = """table name: tasks
            Column name Status : ['To Do', 'In Progress', 'Terminated/Cancelled', 'Development',
            'Development Complete', 'Done', 'Ready for QC', 'Discovery Phase',
            'QA level 1 Completed', 'QC Passed', 'QA Completed', 'Hold',
            'QA level 2 in progress']
            Other column names: ['Task ID', 'Task Name', 'Owner', 'Priority', 'Start Date', 'Due Date',
            'Created Time', 'Status', 'Is Overdue', 'Completion Percentage',
            'Project Name', 'Milestone Name', 'Project ID', 'Milestone ID',
            'Parent Task ID', 'Created By ID', 'Owner IDs', 'Task Delay Time',
            'Task Completion Mode', 'Actual Time Taken', 'Time Spent So Far',
            'Duration_1', 'Duration Unit', 'Rate Per Hour', 'Clarity Level',
            'QC Owner']
            """
        elif self.label == 'milestones':
            context = """table name: milestones
            Column name Milestone Status  : ['Upcoming', 'Overdue', 'Completed']
            Other column names: ['Project Name', 'Milestone Name', 'Owner Name', 'Start Date',
            'End Date', 'Milestone Status', 'Milestone ID', 'Owner ID',
            'Project ID', 'Created Time', 'Duration', 'Actual Time Taken',
            'Milestone Completion Mode', 'Milestone ID String',
            'Project ID String']
            """

        cot = ChainOfThoughtRAG(1, table_context=context)
        answer = cot(input_text).answer
        print(answer)
        
        if isinstance(answer, list):
            answer = answer[0]
        
        final_answer = self.query_db.execute_sql(answer)
        print(final_answer)
        final_answer = final_answer.to_json()
        return final_answer

if __name__ == "__main__":
    gr = GetResults("milestones")
    print(gr.get_results(input_text="give me records where milestone status is 'Completed'"))

