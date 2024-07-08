# django-app/Dockerfile
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Run migrations and collect static files
# RUN python manage.py migrate
# RUN python manage.py create_groups

# Expose port 8000 and start the Django server
EXPOSE 8009
CMD ["python", "manage.py", "runserver", "0.0.0.0:8009"]
