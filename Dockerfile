FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Copy app and dependencies
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY app.py /app/

# Expose the Flask app port
EXPOSE 5000

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Command to run the app
CMD ["python", "app.py"]
