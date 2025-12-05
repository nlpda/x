import json
import time
import logging
from .usb_gadget_control import USBGadget

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlaybookRunner:
    """
    Parses and executes a playbook file.
    """

    def __init__(self, playbook_path, gadget):
        self.playbook = self._load_playbook(playbook_path)
        self.gadget = gadget

    def _load_playbook(self, playbook_path):
        """Loads a playbook from a JSON file."""
        logging.info(f"Loading playbook from {playbook_path}...")
        try:
            with open(playbook_path, 'r') as f:
                playbook = json.load(f)
            logging.info(f"Playbook '{playbook.get('name')}' loaded successfully.")
            return playbook
        except FileNotFoundError:
            logging.error(f"Playbook file not found at {playbook_path}")
            return None
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {playbook_path}")
            return None

    def execute(self):
        """Executes the loaded playbook."""
        if not self.playbook:
            logging.error("No playbook loaded, cannot execute.")
            return

        logging.info(f"Executing playbook: {self.playbook['name']}")
        self.gadget.initialize_hid()

        for step in self.playbook.get('steps', []):
            action = step.get('action')
            payload = step.get('payload')
            description = step.get('description', 'No description')

            logging.info(f"Executing step: {description}")

            if action == 'type_string':
                self.gadget.type_string(payload)
            elif action == 'press_keys':
                self.gadget.press_keys(payload)
            elif action == 'delay':
                time.sleep(payload)
            else:
                logging.warning(f"Unknown action type: {action}")

        logging.info("Playbook execution finished.")
        # self.gadget.unregister_gadget()

if __name__ == '__main__':
    from usb_gadget_control import USBGadget

    gadget = USBGadget()
    playbook_path = 'playbooks/offensive_hid_recon.json'
    runner = PlaybookRunner(playbook_path, gadget)
    runner.execute()
