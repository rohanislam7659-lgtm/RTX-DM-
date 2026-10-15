# RTX DM - Facebook Auto Comment Tool

<p align="center">
  <img src="[https://img.shields.io/badge/Python-3.x-blue.svg](https://img.shields.io/badge/Python-3.x-blue.svg)" alt="Python">
  <img src="[https://img.shields.io/badge/Termux-Supported-green.svg](https://img.shields.io/badge/Termux-Supported-green.svg)" alt="Termux">
</p>

**RTX DM** is a powerful Python-based command-line tool designed for Termux to automate comments on Facebook posts using Graph API.

---

## 🚀 Termux Installation Guide

Run the following commands one by one in your Termux terminal:

```bash
# 1. Update and upgrade termux packages
pkg update && pkg upgrade -y

# 2. Install git and python
pkg install git python -y

# 3. Clone this repository
git clone https://github.com/YOUR_USERNAME/RTX-DM.git

# 4. Navigate to the project directory
cd RTX-DM

# 5. Install required dependencies
pip install -r requirements.txt

# 6. Run the tool
python main.py
