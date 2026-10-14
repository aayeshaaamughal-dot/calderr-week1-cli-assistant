
from code_review_agent import review_code


TEST_CASES = [
    {
        "name": "Division by zero",
        "code": "print(10 / 0)",
    },
    {
        "name": "Hard-coded password",
        "code": 'password = "admin123"\nprint(password)',
    },
    {
        "name": "Empty function",
        "code": "def process_data():\n    pass",
    },
    {
        "name": "File handling",
        "code": (
            "file = open('data.txt', 'r')\n"
            "content = file.read()\n"
            "print(content)"
        ),
    },
    {
        "name": "Clean addition function",
        "code": (
            "def add(a, b):\n"
            "    return a + b\n"
            "\n"
            "print(add(2, 3))"
        ),
    },
]


if __name__ == "__main__":
    for number, test in enumerate(TEST_CASES, start=1):
        print(f"\n{'=' * 50}")
        print(f"TEST {number}: {test['name']}")
        print("=" * 50)

        try:
            report = review_code(test["code"])
            print("Summary:", report.overall_summary)
            print("Issues found:", len(report.issues))
            print("Overall risk:", report.overall_risk)
        except Exception as error:
            print("Test failed:", type(error).__name__, error)
