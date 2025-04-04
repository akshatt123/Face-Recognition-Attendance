# 🌟 Face Recognition Attendance System

A full-stack AI-powered attendance system that uses face recognition technology to mark attendance in real-time. Built with Python (Flask), HTML/CSS/JS, and PostgreSQL, this project is containerized using Docker and deployed with Kubernetes (Minikube). The system is highly scalable and easily extensible for educational institutions and enterprises.

---

## 📁 Project Structure

```
Face-Recognition-Attendance/
│
├── frontend/                # Frontend files (HTML/CSS/JS)
│   ├── Dockerfile
│   ├── templates
|   |    |── index.html
│   |── static
|   |    ├── styles.css
│   |    └── script.js
|   └── nginx.conf
│
├── backend/                 # Backend logic (Flask + Face Recognition)
│   ├── Dockerfile
│   ├── app.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── config.py           # (Ignored if contains secrets)
│   ├── requirements.txt
│   ├── face_recognition_utils.py
│   ├── attendance.csv      # Output CSV (ignored in git)
|   |── face_encodings/     # Folder for face images
│   └── environment.yml
│   
|
├── deployment/             # Kubernetes deployment files
│   ├── Dockerfile
│   ├── backend-deployment-2022bcd0033.yaml
│   ├── backend-service-2022bcd0033.yaml
│   ├── frontend-deployment-2022bcd0033.yaml
│   ├── frontend-service-2022bcd0033.yaml
│   ├── db-configmap-2022bcd0033.yaml
│   ├── db-secret-2022bcd0033.yaml      # (Ignored for security)
│   ├── db-persistentvolume-2022bcd0033.yaml
│   ├── db-persistentvolumeclaim-2022bcd0033.yaml
|   └── db-deployment-2022bcd0033.yaml
│
├── docker-compose.yml      # For local container orchestration
├── environment.yml         # Conda environment config
|── requirements.txt        # if you are not using conda
└── README.md               # This file
```

---

## 🚀 Features

- ✅ Real-time face recognition using OpenCV and `face_recognition`
- ✅ Automatic CSV attendance marking
- ✅ Frontend UI to initiate recognition
- ✅ REST API backend using Flask
- ✅ Containerized with Docker for portability
- ✅ Deployed via Kubernetes (Minikube)
- ✅ PostgreSQL backend for scalable data storage
- ✅ Secure environment management with `.env` and Kubernetes secrets

---

## 🤔 Technologies Used

| Layer       | Technology                 |
| ----------- | -------------------------- |
| Frontend    | HTML, CSS, JavaScript      |
| Backend     | Python, Flask              |
| AI Engine   | `face_recognition`, OpenCV |
| Database    | PostgreSQL                 |
| DevOps      | Docker, Kubernetes         |
| Deployment  | Minikube                   |
| Config Mgmt | ConfigMap, Secret, PVC     |

---

## ⚙️ Setup Instructions

### 🐍 1. Clone the Repository

```bash
git clone https://github.com/your-username/Face-Recognition-Attendance.git
cd Face-Recognition-Attendance
```

### 🧪 2. Set Up Environment

Using Conda:

```bash
conda env create -f environment.yml
conda activate face_env
```

### 🧠 3. Local Backend Run (Optional)

```bash
cd backend
python app.py
```

### 🌐 4. Local Frontend Run (Optional)

Just open `frontend/index.html` in a browser.

---

## 🐳 Docker Setup

### 📦 Build Images

```bash
docker-compose build
```

### ▶️ Run Containers

```bash
docker-compose up
```

Frontend → [http://localhost:3000](http://localhost:3000)<br>
Backend API → [http://localhost:5000](http://localhost:5000)

---

## ☘️ Kubernetes Deployment (Minikube)

### ✅ 1. Start Minikube

```bash
minikube start --driver=docker
```

### 🛥️ 2. Enable Ingress (optional if using NGINX)

```bash
minikube addons enable ingress
```

### 📕 3. Apply All Configurations

```bash
kubectl apply -f deployment/
```

### 📱 4. Access the Frontend

```bash
minikube service frontend-service --url
```

Use the provided URL to access the application.

---

## 🧠 How It Works

1. Add training images to `backend/face_encodings/` (e.g., `person1.jpg`, `person2.jpg`).
2. Run the system.
3. The camera captures a live stream, compares faces using encodings.
4. If a match is found, attendance is marked in `attendance.csv` and pushed to the PostgreSQL database.
5. A visual confirmation is also displayed on the frontend that the attendance has been successfully marked.


## 📋 Future Improvements

- 📦 Add UI dashboard for admin management
- 🔒 Role-based access control
- 📊 Graphs for attendance analytics

---

##

