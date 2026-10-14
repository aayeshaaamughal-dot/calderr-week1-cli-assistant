
import subprocess
import sys

TESTS = [
    {
        "name": "Program starts",
        "input": "/exit\n",
        "expected": "Intelligent CLI Assistant",
    },
    {
        "name": "Help command",
        "input": "/help\n/exit\n",
        "expected": "Available Commands",
    },
    {
        "name": "Show default topic",
        "input": "/topic\n/exit\n",
        "expected": "General conversation",
    },
    {
        "name": "Change topic",
        "input": "/topic Python\n/exit\n",
        "expected": "Topic changed to: Python",
    },
    {
        "name": "Clear memory command",
        "input": "/clear\n/exit\n",
        "expected": "Conversation memory cleared",
    },
    {
        "name": "Ignore blank input",
        "input": "\n/exit\n",
        "expected": "Goodbye",
    },
    {
        "name": "Exit command",
        "input": "/exit\n",
        "expected": "Goodbye",
    },
]

passed = 0

print("\nCLI Assistant Basic Evaluation")
print("=" * 35)

for test in TESTS:
    result = subprocess.run(
        [sys.executable, "cli_assistant.py"],
        input=test["input"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    output = result.stdout + result.stderr
    success = test["expected"].lower() in output.lower()

    if success:
        passed += 1

    print(
        f"{'PASS' if success else 'FAIL'} - {test['name']}"
    )

print("=" * 35)
print(f"Result: {passed}/{len(TESTS)} tests passed")
print(
    "Note: These are basic command checks, "
    "not the full 10-turn AI quality evaluation."
)
