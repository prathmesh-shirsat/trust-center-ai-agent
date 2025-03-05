import asyncio
import json
from agents.agent_runner import AgentRunner
from utils.llm import llmInstance

def load_request(file_path):
    """Loads and parses the request.json file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading request file: {e}")
        return None

async def main():
    request_data = load_request("config/asanaRequest.json")

    # Run agent for the single request
    agent_runner = AgentRunner(request_data, llmInstance)
    result = await agent_runner.run_all_agents()

    # Structure the final output
    final_output = result if isinstance(result, dict) else {"results": []}

    # Save the formatted JSON response to a file
    with open("output/asana_final_output.json", "w", encoding="utf-8") as file:
        json.dump(final_output, file, indent=4)

if __name__ == '__main__':
    asyncio.run(main())
