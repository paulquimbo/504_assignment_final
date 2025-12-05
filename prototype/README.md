## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
Make sure `requirements.txt` is in the project root, then run:
```bash
pip install -r requirements.txt
```

### 4. Run the Application Locally
```bash
python app.py
```

The app will start on `http://127.0.0.1:8000` by default.

---

## Deploying to Azure (Work in Progress)

At this stage, deployment to Azure App Service is still being tested.  
These are the steps being followed, but errors are currently under investigation:

1. Prepare your project folder with:
   - `app.py` (entry point of the Flask app)
   - `requirements.txt` (all dependencies listed)

2. In the Azure Portal:
   - Go to **App Services → Deployment Center → Zip Deploy**.
   - Upload a zip of your project folder.

3. If your `app.py` is inside a subfolder (e.g., `prototype/app.py`), configure the **Startup Command** under **Configuration → General settings**:
   ```bash
   python prototype/app.py

## Reproducibility Notes
- All dependencies are listed in `requirements.txt`.
- The app runs on Python 3.10 (tested).
- Use `venv` to isolate environments and ensure consistent results.
- Deployment steps are documented for Azure App Service.

---
