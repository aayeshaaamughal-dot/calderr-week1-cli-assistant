
import os
import json
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY .env file mein nahi mili."
    )

client = Groq(api_key=api_key)


class JobPosting(BaseModel):
    job_title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    salary_range: Optional[str] = Field(
        default=None,
        description="Salary range, if mentioned"
    )
    skills: list[str] = Field(
        description="Required skills"
    )
    location: str = Field(description="Job location")
    remote_status: str = Field(
        description="Remote, Hybrid, On-site, or Not specified"
    )



job_text = """
We are hiring a Junior Python Developer at CodeCraft.
Location: Lahore, Pakistan.
Required skills: Python, SQL.
Work arrangement: Remote.
"""


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": (
                "Extract job information from the provided text. "
                "Return only valid JSON with these keys: "
                "job_title, company, salary_range, skills, "
                "location, remote_status. "
                "Use null for missing salary_range, an empty list "
                "for missing skills, and 'Not specified' for "
                "missing location or remote_status. "
                "Do not invent information."
            )
        },
        {
            "role": "user",
            "content": job_text
        }
    ],
    response_format={"type": "json_object"},
    temperature=0
)

result = json.loads(response.choices[0].message.content)

validated_job = JobPosting.model_validate(result)

print("\nAI-EXTRACTED JOB DETAILS")
print(validated_job.model_dump_json(indent=2))
