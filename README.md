# AI-Driven USB Security Tool (Project Chimera)

## Overview

Project Chimera is a proof-of-concept tool that uses a Raspberry Pi Zero W2 as an AI-orchestrated USB device. It can dynamically switch between offensive and defensive security roles, driven by natural language commands. This tool is intended for professional security research, authorized red-teaming, and incident response training.

This initial version (Phase 1) implements a basic offensive HID attack, where the AI selects and executes a playbook to run reconnaissance commands on a target host.

## Features (Phase 1)

*   **AI-Powered Decision Making**: Utilizes a cloud-based LLM (like GPT) to interpret natural language commands and select the appropriate action.
*   **Playbook-Driven Actions**: All operations are defined in simple JSON playbooks, ensuring actions are predictable and controlled.
*   **Simulated HID Attack**: The PoC includes a playbook to emulate a keyboard (HID) and run basic commands (`hostname`, `whoami`) on a Windows target.
*   **Modular Architecture**: The code is structured to easily support new playbooks, different USB gadget modes (e.g., Ethernet, mass storage), and alternative AI models in the future.

## How It Works

1.  **Operator Command**: The user provides a high-level command (e.g., `"run a recon scan"`).
2.  **AI Playbook Selection**: The `DecisionEngine` sends the command and a list of available playbooks to the AI, which chooses the best match.
3.  **Playbook Execution**: The `PlaybookRunner` reads the chosen JSON playbook.
4.  **USB Gadget Control**: The `USBGadget` module translates the playbook steps into low-level commands to control the Raspberry Pi's USB port, emulating a keyboard to execute the attack.

## Setup and Installation

### Prerequisites

*   A Raspberry Pi Zero W2 (or other OTG-capable Pi)
*   Raspberry Pi OS with SSH and network connectivity
*   Python 3.8+
*   An OpenAI API key (or another compatible cloud AI service)

### Step 1: Configure the Raspberry Pi for USB Gadget Mode

1.  **Enable `dwc2` Overlay**:
    Add `dtoverlay=dwc2` to the end of your `/boot/config.txt` file.

2.  **Enable `libcomposite`**:
    Add `libcomposite` to a new line in `/etc/modules`.

3.  **Reboot the Pi**:
    `sudo reboot`

### Step 2: Deploy the Code

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Configure the Environment

1.  **Set the API Key**:
    You must set your OpenAI API key as an environment variable. You can add this to your `~/.bashrc` for persistence.
    ```bash
    export OPENAI_API_KEY="your_secret_api_key_here"
    source ~/.bashrc
    ```

## Usage

Connect the Raspberry Pi's USB OTG port to the target machine. Once the device is recognized, run the tool via SSH.

**Example:**

To execute the basic reconnaissance playbook, run the following command from the project's root directory on the Pi:

```bash
python3 -m src.main "run a basic recon on the target machine"
```

The tool will then:
1.  Initialize the USB gadget as a keyboard.
2.  Open the Windows Run dialog (`Win + R`).
3.  Type `powershell` and press Enter.
4.  Wait for the terminal to open.
5.  Type the recon commands and execute them.

## Development Notes

*   The `usb_gadget_control.py` module is currently in **simulation mode**. It logs the commands it *would* run on a real Pi. To make it functional, you will need to uncomment the `subprocess.run()` calls and replace the logging.
*   The AI's choice is simulated in `ai_engine.py` to avoid unnecessary API calls during development. To use the live AI, you'll need to implement the actual API call and parse the response.

---
**Disclaimer**: This tool is for educational and authorized professional use only. Unauthorized use against systems is illegal.
