import os
import logging
import json
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DecisionEngine:
    """
    Uses an AI model to select the appropriate playbook based on a natural language command.
    """

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=api_key)

    def _get_available_playbooks(self, playbook_dir='playbooks'):
        """Scans the playbook directory and returns a list of available playbooks."""
        playbooks = []
        for filename in os.listdir(playbook_dir):
            if filename.endswith('.json'):
                playbook_path = os.path.join(playbook_dir, filename)
                try:
                    with open(playbook_path, 'r') as f:
                        data = json.load(f)
                        playbooks.append({
                            "filename": filename,
                            "name": data.get("name"),
                            "description": data.get("description")
                        })
                except (json.JSONDecodeError, IOError) as e:
                    logging.warning(f"Could not read or parse playbook {filename}: {e}")
        return playbooks

    def choose_playbook(self, command):
        """
        Chooses a playbook based on the user's command.
        """
        playbooks = self._get_available_playbooks()
        if not playbooks:
            logging.error("No playbooks available.")
            return None

        prompt = self._construct_prompt(command, playbooks)

        logging.info("--- AI PROMPT ---")
        logging.info(prompt)
        logging.info("--------------------")

        # --- Live API Call (Example) ---
        # To enable the live AI, comment out the simulation block below and uncomment this.
        # try:
        #     response = self.client.chat.completions.create(
        #         model="gpt-4",
        #         messages=[{"role": "user", "content": prompt}],
        #         temperature=0,
        #     )
        #     chosen_playbook_filename = response.choices[0].message.content.strip()
        #     logging.info(f"AI chose playbook: {chosen_playbook_filename}")
        #
        #     # Basic validation to ensure the file exists in the playbook directory
        #     if os.path.exists(os.path.join('playbooks', chosen_playbook_filename)):
        #         return os.path.join('playbooks', chosen_playbook_filename)
        #     else:
        #         logging.error(f"AI chose a non-existent playbook: {chosen_playbook_filename}")
        #         return None
        # except Exception as e:
        #     logging.error(f"Error calling OpenAI API: {e}")
        #     return None
        # --------------------------------

        # --- Simulation Block (for PoC) ---
        logging.info("Using simulated AI response.")
        if "recon" in command.lower() or "whoami" in command.lower():
            chosen_playbook_filename = "offensive_hid_recon.json"
            logging.info(f"SIMULATED AI RESPONSE: Chose '{chosen_playbook_filename}'")
            return os.path.join('playbooks', chosen_playbook_filename)

        logging.warning("SIMULATED AI: No suitable playbook found for the command.")
        return None


    def _construct_prompt(self, command, playbooks):
        """Constructs the prompt for the AI model."""
        playbook_list = "\n".join([
            f"- {p['filename']}: {p['name']} ({p['description']})" for p in playbooks
        ])

        return f"""
You are an AI assistant for a cybersecurity tool. Your task is to select the best playbook to execute based on the user's command.

The user's command is: "{command}"

Here are the available playbooks:
{playbook_list}

Based on the user's command, which playbook file should be executed?
Return only the filename of the chosen playbook (e.g., "playbook.json"). Do not provide any other text or explanation.
"""

if __name__ == '__main__':
    # This requires an environment variable OPENAI_API_KEY to be set.
    # For the test, we'll use a dummy key since the API call is simulated.
    api_key = os.environ.get("OPENAI_API_KEY", "dummy_key_for_testing")

    engine = DecisionEngine(api_key=api_key)

    # Test case 1: A command that should match our playbook
    command = "Run a basic recon on the target machine."
    print(f"\nTesting with command: '{command}'")
    chosen = engine.choose_playbook(command)
    print(f"Chosen playbook: {chosen}")

    # Test case 2: A command that should not match
    command = "Backup all files."
    print(f"\nTesting with command: '{command}'")
    chosen = engine.choose_playbook(command)
    print(f"Chosen playbook: {chosen}")
