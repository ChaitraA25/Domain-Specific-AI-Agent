from services.llm_service import generate_answer

answer = generate_answer(
    question = "What is FastAPI?",

    context="""
    FastAPI is a modern Python framework
    for building APIs.
"""
)
print(answer)