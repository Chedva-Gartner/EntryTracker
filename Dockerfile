FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy app and dependencies
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Copy application code
COPY --chown=appuser:appuser app.py .

# Change ownership of working directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the Flask app port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
