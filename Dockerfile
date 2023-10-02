FROM python:3.10-slim

# Create working folder and install dependencies
WORKDIR /app

ADD https://github.com/NREL/EnergyPlus/releases/download/v22.2.0/EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu22.04-x86_64.tar.gz EnergyPlus-22.2.0
RUN tar -xvzf EnergyPlus-22.2.0

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY ./ ./

# Switch to a non-root user
# RUN useradd --uid 1000 manav && chown -R manav /app
# USER manav

# Run the service
EXPOSE 7000
CMD ["gunicorn", "--bind=0.0.0.0:7000", "--log-level=info", "service:app"]