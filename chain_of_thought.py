from data_reader import excel_reader
import dspy
import os
# os.environ['LLM_API_KEY']=""
api_key = os.getenv('OPENAI_API_KEY')
os.environ['LLM_API_KEY']=api_key
os.environ['MODEL_NAME']="gpt-3.5-turbo"
# tasks_path = ""
# tasks=excel_reader(tasks_path)

# milestone_path = ""
# milestone = excel_reader(tasks_path)

def set_llm():
    lm = dspy.OpenAI(model=os.environ['MODEL_NAME'],api_key=os.environ['LLM_API_KEY'])
    return lm

class RAGSignature(dspy.Signature):
    """INSTRUCTION: You are a SQL EXPERT with unlimited experience, you never get wrong and follow the instructions, Provide SQL queries based on given question and only give CODE and NO MARKDOWN like ```sql``` or else huge penalty
    if you encounter any human name try to find a substring match also, if you get dates data then format it to sql format and then answer,
    make sure you follow the given column names EXACTLY Do not merge them, limit the use of limiters like top and limit"""

    context = dspy.InputField(desc="You will be given a sample row which will contain flattened values of table in the format column name: Value lookout for synonyms as well")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="SQL code only ensuring you follow strict SQL guidelines and syntax")

class ChainOfThoughtRAG(dspy.Module):
    
    def __init__(self, context_length, table_context):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=context_length)
        self.generate_answer = dspy.ChainOfThought(RAGSignature)
        self.k = context_length
        self.context = table_context

    def forward(self, question):
        # context = generate_context(question, k=self.k) df.columns
        prediction = self.generate_answer(context=self.context, question=question)
        return dspy.Prediction(context=self.context, answer=prediction.answer)

class RAGSignatureSQL(dspy.Signature):
    """INSTRUCTION: You are a SQL EXPERT with unlimited experience, you never get wrong and follow the instructions, Provide Correct refind SQL queries based on given input and only give CODE and NO MARKDOWN like ```sql``` or else huge penalty
    if you encounter any human name try to find a substring match also, if you get dates data then format it to sql format and then answer,
    make sure you follow the given column names EXACTLY Do not merge them, limit the use of limiters like top and limit
    
    Main instruction: Apply inverted commas on columns while making the query "column 1" """

    context = dspy.InputField(desc="You will be given a sample row which will contain flattened values of table in the format column name: Value lookout for synonyms as well")
    question = dspy.InputField(desc="This will contain the generated SQL query, refine it to perfection")
    answer = dspy.OutputField(desc="SQL code only ensuring you follow strict SQL guidelines and syntax")
    
class ChainOfThoughtSQLCorrect(dspy.Module):
    
    def __init__(self, context_length, table_context):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=context_length)
        self.generate_answer = dspy.ChainOfThought(RAGSignatureSQL)
        self.k = context_length
        self.context = table_context

    def forward(self, question):
        # context = generate_context(question, k=self.k) df.columns
        prediction = self.generate_answer(context=self.context, question=question)
        return dspy.Prediction(context=self.context, answer=prediction.answer)
