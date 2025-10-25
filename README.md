# AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM

An **AI-DRIVEN CSPM (CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM)** That scans simulated and real cloud configurations (AWS/AZURE/GCP), detects misconfigurations, and provides beautiful **DASHBOARD UI** FOO VISUALIZATION + **COMMAND LINE REPORTS** 🚀

---

## ✨ FEATURES

- ✅ **AI-POWERED RISK DETECTION** (ML-BASED ANOMALY DETECTION)
- ✅ **CLOUD CONFIG SCANNER** (AWS/AZURE/GCP SIMULATED SCANS)
- ✅ **DUAL OUTPUT:** CMD (CONSOLE) + WEB BROWSER (REACT UI)
- ✅ **INTERACTIVE DASHBOARD:** RISK SCORES , GRAPHS , COLORED ALERTS
- ✅ **CUSTOM REPORTS:** JSON + CSV + WEB VIEW

---

## 📂 FOLDER STRUCTURE

AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ db.py
│  │  ├─ schemas.py
│  │  ├─ ai_detector.py
│  │  ├─ sample_data.py
│  │  └─ requirements.txt
│  ├─ Dockerfile
│  └─ entrypoint.sh
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx
│     ├─ api.js
│     └─ styles.css
├─ docker-compose.yml
└─ README.md


---

# ⚙️ SETUP AND INSTALLATION

## BACKEND (PYTHON)
D: 
CD AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM 
CD BACKEND 
pip install -r requirements.txt

## FRONTEND (REACT)
D:
CD AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM
CD FRONTEND
npm install 
npm start

**NOTE: BE CAREFUL IF WE WANT OUTPUT TO VIEW IN WEB BROWESER FIRST WE HAVE TO RUN IN CMD AND PARALLEL WE HAVE TO OPEN THE LINK PROVIDED**

**IF WE WANT TO VIEW THE OUTPUT FIRST WE HAVE TO RUN IN CMD AND COPY AND PASTE ONLY THIS http://127.0.0.1:8000 IN CHROME AND IT WILL SHOW BACKEND SUCCESSFULLY COMPILED AND THEM SIMULTANEOUSLY PASTE THIS http://127.0.0.1:8000 IN CHROME TO VIEW THE OUTPUT**

## ▶️ RUN THE PROJECT
Open CMD / Terminal →  uvicorn app.main:app --reload --port 8000

Open Web Browser → http://127.0.0.1:8000/docs#/
open this link to VIEW

Get dual output:

📟 CMD → logs + security findings

🌐 Browser → colorful dashboard with graphs & tables

## 📊 Example Outputs

CMD Output
(venv) D:\PROJECTS REHAN\AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM\backend> uvicorn app.main:app --reload --port 8000
INFO:     Will watch for changes in these directories: ['D:\\PROJECTS REHAN\\AI-POWERED-CLOUD-SECURITY-POSTURE-MANAGEMENT-SYSTEM-CSPM\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


Web Dashboard
http://127.0.0.1:8000/docs#/
You’ll see the Swagger API Interface, titled:
AI CSPM API BY D.REHAN SAI RITHVIK
It will show all available endpoints such as:

/resources

/findings

/detect

/scan (depending on your final code)

You can click “Try it out” and test them there itself.

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🧑‍💻 Developed By
👨‍💻 DASIKA REHAN SAI RITHVIK

B.Sc. (Hons) in Computer Science – Nizam College Autonomous (Osmania University)
Email: rehansairithvikdasika@gmail.com
Mobile Number: 9581277713