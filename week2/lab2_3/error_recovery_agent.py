
import time
import logging
import random
from datetime import date

# Save error and retry information in a log file.
logging.basicConfig(
    filename="agent_errors.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Simulate an unreliable primary tool.
def primary_tool():
    if random.random() < 0.7:
        raise ConnectionError("Simulated temporary connection failure")
    return "Primary tool succeeded!"


# Alternative tool if the primary tool keeps failing.
def fallback_tool():
    return "Fallback tool succeeded!"


def run_with_retries(tool, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            result = tool()
            logging.info(
                "%s succeeded on attempt %s",
                tool.__name__,
                attempt,
            )
            return result

        except Exception as error:
            logging.warning(
                "%s failed on attempt %s: %s",
                tool.__name__,
                attempt,
                error,
            )
            print(f"Attempt {attempt} failed: {error}")

            if attempt < max_attempts:
                # Exponential backoff: 1, 2, 4 seconds...
                delay = 2 ** (attempt - 1)
                print(f"Retrying in {delay} second(s)...")
                time.sleep(delay)

    logging.error("%s failed after all attempts", tool.__name__)
    return None


def main():
    print("ERROR RECOVERY AGENT")
    print("1. Test automatic retry and fallback")
    print("2. Test date tool")
    print("3. Exit")

    while True:
        choice = input("\nChoose 1, 2, or 3: ").strip()

        if choice == "1":
            result = run_with_retries(primary_tool)

            if result is None:
                print("Primary tool failed. Trying fallback...")
                result = run_with_retries(fallback_tool)

            print("Final result:", result)

        elif choice == "2":
            print("Today's date:", date.today().isoformat())

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
