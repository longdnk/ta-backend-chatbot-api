from model.llm import llm
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
### Question Re-writer

# Prompt
re_write_prompt = PromptTemplate(
    template="""You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the initial and formulate an improved question. \n
     Hint: If the original question asks "momo ra đời vào năm nào"/"momo ra đời năm nào", transform it to "momo được thành lập năm nào" for clarity.
     Here is the initial question: \n\n {question}. Improved question with no preamble: \n 
    """,
    input_variables=["generation", "question"],
)

question_rewriter = re_write_prompt | llm | StrOutputParser()