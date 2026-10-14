
import os
import json
from datetime import date
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY .env file mein nahi mili.")

client = Groq(api_key=api_key)


# TOOL 1: Mock web search
def web_search_mock(query: str) -> str:
    return (
        f"Mock search results for '{query}': "
        "Result 1: Official documentation; "
        "Result 2: Educational guide; "
        "Result 3: Recent overview. "
        "These are demonstration results, not live web results."
    )


# TOOL 2: Safe basic calculator
def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/(). %")
    if not expression or any(ch not in allowed for ch in expression):
        return "Error: Only basic arithmetic characters are allowed."

    try:
        # No eval(): parse only basic arithmetic with Python AST.
        import ast
        import operator

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
            ast.Mod: operator.mod,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                return operators[type(node.op)](
                    evaluate(node.left), evaluate(node.right)
                )
            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.operand))
            raise ValueError("Unsupported arithmetic expression")

        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree)
        return str(result)
    except Exception:
        return "Error: Invalid arithmetic expression."


# TOOL 3: Current date
def get_current_date() -> str:
    return date.today().isoformat()


# TOOL 4: Text summarizer
def summarize(text: str) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return ". ".join(sentences[:2]) + ("." if sentences else "")


# TOOL 5: Simple sentiment classifier
def classify_sentiment(text: str) -> str:
    positive = {"good", "great", "excellent", "happy", "love", "useful"}
    negative = {"bad", "poor", "terrible", "sad", "hate", "useless"}

    words = set(text.lower().replace(".", " ").replace(",", " ").split())
    score = len(words & positive) - len(words & negative)

    if score > 0:
        return "Positive"
    if score < 0:
        return "Negative"
    return "Neutral"


TOOLS = {
    "web_search_mock": {
        "function": web_search_mock,
        "description": "Search a topic using mock demonstration results.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    "calculate": {
        "function": calculate,
        "description": "Calculate a basic arithmetic expression.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    "get_current_date": {
        "function": get_current_date,
        "description": "Get today's date. Takes no arguments.",
        "parameters": {"type": "object", "properties": {}},
    },
    "summarize": {
        "function": summarize,
        "description": "Summarize text into its first two sentences.",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    "classify_sentiment": {
        "function": classify_sentiment,
        "description": "Classify text as Positive, Negative, or Neutral.",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
}


def run_agent(user_request: str) -> None:
    tool_specs = []

    for name, info in TOOLS.items():
        tool_specs.append({
            "type": "function",
            "function": {
                "name": name,
                "description": info["description"],
                "parameters": info["parameters"],
            },
        })

    messages = [
        {
            "role": "system",
            "content": (
                "You are a research assistant. Select the most suitable "
                "tool for the user's request. Call a tool when useful. "
                "For arithmetic, use calculate. For today's date, use "
                "get_current_date. For summaries, use summarize. For "
                "sentiment, use classify_sentiment. For topic searches, "
                "use web_search_mock. Do not claim mock search is live."
            ),
        },
        {"role": "user", "content": user_request},
    ]

    for _ in range(5):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tool_specs,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("\nAGENT RESPONSE")
            print(message.content or "No text response.")
            return

        for tool_call in message.tool_calls:
            name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
                if name not in TOOLS:
                    result = "Error: Unknown tool."
                else:
                    result = TOOLS[name]["function"](**arguments)
            except Exception as error:
                result = f"Tool error: {error}"

            print(f"\nTool used: {name}")
            print(f"Tool result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    print("\nAgent stopped after 5 tool-call rounds.")


if __name__ == "__main__":
    print("MULTI-TOOL RESEARCH AGENT")
    print("Type 'exit' to quit.")

    while True:
        request = input("\nYour request: ").strip()
        if request.lower() == "exit":
            break
        if request:
            run_agent(request)
