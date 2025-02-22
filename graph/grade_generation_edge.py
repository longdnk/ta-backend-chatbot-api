from schema.answer_grader import answer_grader
from graph.message_state import update_message_state
from schema.hallucination_grader import hallucination_grader

def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    # print("Check halu: ",state)
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    grade = score["score"]

    # # Check hallucination
    # if grade == "yes":
    #     print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
    #     # Check question-answering
    #     print("---GRADE GENERATION vs QUESTION---")
    #     score = answer_grader.invoke({"question": question, "generation": generation})
    #     grade = score["score"]
    #     if grade == "yes":
    #         print("---DECISION: GENERATION ADDRESSES QUESTION---")
    #         return "useful"
    #     else:
    #         print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
    #         return "not useful"
    # else:
    #     print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
    #     return "not supported"

    # Check hallucination
    result = 'useful'
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score["score"]
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            result =  "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            result =  "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        result =  "not supported"

    # Store the result in the state so it can be accessed later
    state["generation_result_message"] = f"Generation result: {result.replace('_', ' ').title()}"
    update_message_state(result.replace('_', ' ').title())
    # print(state["generation_result_message"])
    return result