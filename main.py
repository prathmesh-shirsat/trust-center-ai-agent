import asyncio
import json
from agents.agent_runner import AgentRunner
from utils.llm import llmInstance
from utils.constants import AGENT_TIMEOUT  # Import timeout correctly


def load_task(file_path):
    """Loads the task as a string from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Error loading task file: {e}")
        return None

async def main(task_file):
    task = load_task(task_file)
    if not task:
        print("No valid task found. Exiting...")
        return
    
    agent_runner = AgentRunner(task, llmInstance)
    agent_runner.create_agent()

    task_execution = asyncio.create_task(agent_runner.run())
    timeout_task = asyncio.create_task(agent_runner.stop_agent_after_timeout(AGENT_TIMEOUT))

    done, pending = await asyncio.wait(
        [task_execution, timeout_task], return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel timeout if agent finishes first
    if timeout_task in pending:
        timeout_task.cancel()

    final_result = task_execution.result() if task_execution in done else {"status": "error", "message": "Timed out"}

    print(final_result)
    with open("output/final_output.json", "w", encoding="utf-8") as file:
        json.dump(final_result, file, indent=4)
    
    return final_result


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <task_file>")
    else:
        task_file = sys.argv[1]
        asyncio.run(main(task_file))
