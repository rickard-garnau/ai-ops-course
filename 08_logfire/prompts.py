import logfire
from logfire import VariablesOptions
from dotenv import load_dotenv
import os

load_dotenv()

logfire.configure(api_key=os.environ["LOGFIRE_API"], variables=VariablesOptions())

def get_prompt(
    name: str="coach_agent_instructions", 
    default: str = "jokey assistant", 
    label: str = "production",
):
    prompt = logfire.var(name=f"prompt__{name}", type=str, default=default)
    prompt.refresh_sync(force=True)
    resolved = prompt.get(label=label)

    return resolved.value

if __name__ == "__main__":
    prompt = get_prompt(label="dev")
    print(prompt)

    report = logfire.variables_validate()
    print(report.format())