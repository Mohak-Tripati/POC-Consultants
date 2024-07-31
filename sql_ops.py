# import psycopg2
# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# from langchain_community.utilities.sql_database import SQLDatabase
# from crewai_tools import tool

# def run_sql_query(sql_query, label):
#     # if label=="milestones":
#     #     db_name = "sqlite:///milestones.db"
#     # else:
#     db_name = "postgresql://postgres:qwerty@localhost:5432/postgres"
#     db = SQLDatabase.from_uri(db_name)
#     print(db)
#     @tool("execute_sql")
#     def execute_sql(sql_query: str) -> str:
#         """Execute a SQL query against the database. Returns the result"""
#         return QuerySQLDataBaseTool(db=db).invoke(sql_query)
#     return execute_sql.run(sql_query)

# if __name__ == "__main":
#     print(run_sql_query("""SELECT DISTINCT "Project Name" FROM milestones WHERE "Owner Name" LIKE '%Waheeba%'"""))