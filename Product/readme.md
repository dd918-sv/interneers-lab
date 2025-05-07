# Setup Python Virtual environment on Linux
```
python3 -m venv .venv
source .venv/bin/activate
```

# Install Python Dependencies
```
pip install -r requirements.txt
```

# Setup MongoDB with Docker
```
docker-compose up -d
```

# Setup React Frontend
```
cd react-app
npm install
```

# Seeding data
```
python3 -m product.seed
```
The server itself seeds itself on startup using this seed.py 

# Run django backend server
```
python3 manage.py runserver
```
Backend server will start at http://127.0.0.1:8000/

# Run react development server
```
cd react-app
npm run dev
```
Frontend will start at http://localhost:5173

