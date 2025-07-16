@echo off
echo Starting Django-Vue.js Development Environment...

REM Start PostgreSQL container
echo Starting PostgreSQL container...
podman compose -f db/compose.yml up -d

REM Wait for PostgreSQL to be ready
echo Waiting for PostgreSQL to start...
timeout /t 10 /nobreak >nul

REM Start Django development server
echo Starting Django backend...
start cmd /k "cd shroo && python manage.py runserver 80"

REM Start Vue.js development server
echo Starting Vue.js frontend...
start cmd /k "cd shroovue && npm run dev"

echo Development servers started!
echo Backend: http://localhost:80
echo Frontend: http://localhost:3000
echo Press any key to continue...
pause >nul