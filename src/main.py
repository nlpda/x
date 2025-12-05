import os
import argparse
import logging
from .ai_engine import DecisionEngine
from .playbook_runner import PlaybookRunner
from .usb_gadget_control import USBGadget

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the AI-driven USB tool.
    """
    parser = argparse.ArgumentParser(description="AI-driven USB security tool.")
    parser.add_argument("command", type=str, help="Natural language command for the tool to execute.")
    args = parser.parse_args()

    # --- 1. Initialize Components ---

    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable not set.")
        return

    try:
        ai_engine = DecisionEngine(api_key=api_key)
        usb_gadget = USBGadget()
    except ValueError as e:
        logging.error(e)
        return

    # --- 2. Use AI to Choose a Playbook ---
    logging.info(f"Received command: '{args.command}'")
    chosen_playbook_path = ai_engine.choose_playbook(args.command)

    if not chosen_playbook_path:
        logging.error("Could not determine a playbook to run for the given command.")
        return

    # --- 3. Execute the Chosen Playbook ---
    logging.info(f"Executing playbook: {chosen_playbook_path}")
    playbook_runner = PlaybookRunner(playbook_path=chosen_playbook_path, gadget=usb_gadget)
    playbook_runner.execute()

    logging.info("Operation complete.")
    # Consider whether to unregister the gadget automatically or based on a command
    # usb_gadget.unregister_gadget()

if __name__ == '__main__':
    # To run this from the project root for testing:
    # OPENAI_API_KEY="your_dummy_key" python3 -m src.main "run a recon scan"
    main()
