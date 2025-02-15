from schema.retrieval_grader import retrieval_grader

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    # for d in documents:
    #     score = retrieval_grader.invoke(
    #         {"question": question, "document": d.page_content}
    #     )
    #     grade = score["score"]
    #     print("grade: ", grade)
    #     if grade == "yes":
    #         print("---GRADE: DOCUMENT RELEVANT---")
    #         filtered_docs.append(d)
    #     else:
    #         print("---GRADE: DOCUMENT NOT RELEVANT---")
    #         continue
    # return {"documents": filtered_docs, "question": question}
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score["score"]
        
        filtered_docs.append({"document": d, "grade":grade})

        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            # filtered_docs.append({"document": d, "grade":grade})
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    return {"documents": filtered_docs, "question": question}