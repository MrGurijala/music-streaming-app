# FastAPI Project

## Installation Instructions

Follow the instructions below to set up the project on different operating systems.

### 1. Install Python 3.x

Make sure Python 3.7 or higher is installed.

- **Windows**: Download and install Python from [here](https://www.python.org/downloads/windows/).
- **Linux**: Use `sudo apt install python3 python3-pip` (Ubuntu-based).
- **macOS**: Use `brew install python3` or download from [python.org](https://www.python.org/downloads/mac-osx/).

### 2. Set up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application

uvicorn main:app --reload
