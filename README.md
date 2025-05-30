# Gudlift Registration

## 1. Overview

This is a **proof of concept (PoC)** for a lightweight competition booking platform.  
The goal is to keep things minimal, efficient, and easy to iterate based on user feedback.

---

## 2. Technologies Used

- **Python 3.x+**
- **[Flask](https://flask.palletsprojects.com/)** – lightweight and flexible web framework
- **[Virtualenv](https://virtualenv.pypa.io/)** – to manage Python environments

We use JSON files for data instead of a database, to keep the project light during this phase.

---

## 3. Getting Started

### Step-by-step installation:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/AlBlanchard/Python_Testing.git
   cd PYTHON_TESTING
   ```

2. **Create a virtual environment**  
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - On **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask app** (no extra dependency required):

   - On **Linux/macOS**:
     ```bash
     export FLASK_APP=server.py
     export FLASK_ENV=development
     flask run
     ```

   - On **Windows CMD**:
     ```cmd
     set FLASK_APP=server.py
     set FLASK_ENV=development
     flask run
     ```

   - On **Windows PowerShell**:
     ```powershell
     $env:FLASK_APP = "server.py"
     $env:FLASK_ENV = "development"
     flask run
     ```

Once running, open the provided local URL (usually `http://127.0.0.1:5000`) in your browser.

> Important: No `.env` or external configuration manager is required. Keep it simple and native.

---

## 4. Current Setup

The app uses two JSON files as its data source:

- `competitions.json` – list of available competitions
- `clubs.json` – list of clubs and login credentials

> You can use the email addresses listed in `clubs.json` to log into the app.

---

## 5. Testing

This project uses [`pytest`](https://docs.pytest.org/) as the testing framework.

### Run tests

To run all tests:

```bash
pytest
```

### Test Guidelines:

- Aim for **at least 80% coverage**
- Favor **unit tests > integration > functional**
- Organize test files clearly into `unit/`, `integration/`, and `functional/`

### Optional coverage tracking:

You can use [`coverage`](https://coverage.readthedocs.io/) to track how much of your code is tested.

Install with:
```bash
pip install coverage
```

Run tests with coverage:
```bash
coverage run -m pytest
coverage report -m
```

### Reset DB:

The DB reset atomaticaly with FLASK_ENV=development
Anyways, if something goes wrong, you can reset the DB :

```bash
flask reset-db
```

---

## 6. Contribution

- Use Git branches named like `feature/your-feature`, `bug/fix-something`, or `improvement/clearer-readme`
- Submit pull requests into the `QA` branch for review
- Only merge into `main` when all tests pass and reviews are complete
