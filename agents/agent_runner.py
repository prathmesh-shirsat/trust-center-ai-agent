import asyncio
import logging
from browser_use import Agent, Browser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentRunner:
    def __init__(self, task, llm):
        """
        Initializes a single agent for the given task.
        :param task: Task in string format.
        :param llm: LLM model instance.
        """
        self.llm = llm
        self.task = task
        self.agent = None

    def create_agent(self):
        """Creates a single agent instance."""
        self.agent = Agent(
            task=self.task,
            llm=self.llm,
            browser=Browser(),
            max_actions_per_step=5
        )
        logger.info("Created agent.")

    async def run(self):
        """Runs the agent asynchronously and returns extracted document data."""
        if not self.agent:
            logger.error("Agent is not initialized. Call create_agent first.")
            return {"status": "error", "message": "Agent not initialized"}
        
        logger.info("Running agent...")
        try:
            result = await self.agent.run()
            logger.info("Agent execution completed.")
            return result.final_result()
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            return {"status": "error", "message": str(e)}
    
    async def stop_agent(self):
        """Stops the agent and closes the browser if it exists."""
        if self.agent:
            self.agent.stop() 
            if self.agent.browser:
                await self.agent.browser.close()  
            self.agent = None

        

    async def stop_agent_after_timeout(self, timeout):
        """Stops the agent after a given timeout."""
        await asyncio.sleep(timeout)
        await self.stop_agent()
        logger.info(f"Agent stopped after {timeout} seconds.")
