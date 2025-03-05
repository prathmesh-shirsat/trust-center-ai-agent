import json
import asyncio
from browser_use import Agent, Browser

class AgentRunner:
    def __init__(self, task, llm):
        """
        Initializes agents with separate browser instances for each keyword.
        :param task: Input JSON defining the organization and keywords.
        :param llm: LLM model instance.
        """
        self.llm = llm
        self.task = task
        self.agents = self.create_agents()

    def create_agents(self):
        """Creates an agent for each keyword with a unique browser instance."""
        from utils.constants import EXTEND_SYSTEM_MESSAGE

        organization_info = self.task["organization"]
        agents = []
        
        for keyword in self.task["keywords"]:
            agent_task = {
                "organization": organization_info,
                "documentName": keyword
            }
            
            agent = Agent(
                task=json.dumps(agent_task) + "\n" + EXTEND_SYSTEM_MESSAGE,
                llm=self.llm,
                browser=Browser(),
                max_actions_per_step=5,
                initial_actions=[
                    {'open_tab': {'url': organization_info["url"]}},
                ]
            )
            agents.append((keyword, agent))

        return agents

    async def run_agent(self, keyword, agent):
        """
        Runs an agent asynchronously and returns extracted document data.
        Agents are already instructed to return results in the required format.
        """
        try:
            result = await agent.run()
            return result.final_result()
        except Exception as e:
            return {"status": "error", "keyword": keyword, "message": str(e)}

    async def run_all_agents(self):
        """Runs all agents concurrently and consolidates document results."""
        tasks = [self.run_agent(keyword, agent) for keyword, agent in self.agents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert JSON strings to dictionaries if needed
        parsed_results = []
        for result in results:
            if isinstance(result, str):  # If result is a JSON string, parse it
                try:
                    parsed_results.append(json.loads(result))
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON: {result}")
            elif isinstance(result, dict):
                parsed_results.append(result)

        print(f"Parsed Results: {parsed_results}")

        # Aggregate public and private documents
        public_docs = []
        private_docs = []

        for result in parsed_results:
            if result.get("status") == "success":
                public_docs.extend(result.get("documents", {}).get("public", []))
                private_docs.extend(result.get("documents", {}).get("private", []))
            elif result.get("status") == "error":
                print(f"Error processing keyword: {result.get('message')}")

        # Final consolidated response
        consolidated_response = {
            "status": "success" if public_docs or private_docs else "error",
            "organization": {
                "id": self.task["organization"].get("id", ""),
                "name": self.task["organization"]["name"],
                "domain": self.task["organization"]["domain"],
                "trust_center_url": self.task["organization"]["url"]
            },
            "documents": {
                "public": public_docs,
                "private": private_docs
            }
        }

        return consolidated_response