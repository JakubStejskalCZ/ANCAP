# Base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code to the container
COPY . .

# Expose the port (optional, useful for development)
EXPOSE 8000

# Command to run the bot
CMD ["python", "bot.py"]
