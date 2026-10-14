
import os
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    console.print(
        "[red]Error: GROQ_API_KEY nahi mili. Apni .env file check karo.[/red]"
    )
    raise SystemExit(1)

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"

history = []
topic = "General conversation"

def show_help():
    console.print("""
[bold cyan]Available Commands[/bold cyan]
  /topic <name>  Change conversation topic
  /topic         Show current topic
  /clear         Clear conversation memory
  /help          Show commands
  /exit          Exit the assistant
""")

console.print(Panel(
    "[bold green]Intelligent CLI Assistant[/bold green]\n"
    "Your AI assistant with conversation memory.\n"
    "Type /help to see commands.",
    title="CalderR Week 1 - Project 1-I-A"
))

while True:
    try:
        user_input = console.input("\n[bold blue]You:[/bold blue] ").strip()

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            console.print("[yellow]Assistant closed. Goodbye![/yellow]")
            break

        if user_input.lower() == "/help":
            show_help()
            continue

        if user_input.lower() == "/clear":
            history.clear()
            console.print("[yellow]Conversation memory cleared.[/yellow]")
            continue

        if user_input.lower().startswith("/topic"):
            new_topic = user_input[len("/topic"):].strip()

            if new_topic:
                topic = new_topic
                history.clear()
                console.print(
                    f"[green]Topic changed to: {topic}[/green]"
                )
                console.print(
                    "[dim]Previous conversation cleared for the new topic.[/dim]"
                )
            else:
                console.print(f"[cyan]Current topic: {topic}[/cyan]")
            continue

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    f"The current conversation topic is: {topic}. "
                    "Answer clearly and accurately. "
                    "If you are unsure, say so."
                ),
            },
            *history,
            {"role": "user", "content": user_input},
        ]

        with console.status("[bold green]AI is thinking..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_completion_tokens=1200,
            )

        answer = response.choices[0].message.content or "(No text response)"
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})

        console.print(Panel(answer, title="AI Assistant", border_style="green"))

        usage = response.usage
        if usage:
            console.print(
                f"[dim]Tokens this turn: "
                f"{usage.prompt_tokens} prompt + "
                f"{usage.completion_tokens} completion = "
                f"{usage.total_tokens} total[/dim]"
            )

    except KeyboardInterrupt:
        console.print("\n[yellow]Assistant interrupted.[/yellow]")
        break
    except Exception as error:
        console.print(f"\n[red]Request failed: {error}[/red]")
        console.print(
            "[yellow]Check your internet, API key and model availability.[/yellow]"
        )
