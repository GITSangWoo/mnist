echo LINE_API_KEY=$LINE_API_KEY >> /etc/environment;
service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload
