FROM python:3.10-slim

RUN apt-get -y update
RUN apt-get -y install libgomp1 libx11-dev

# Create working folder and install dependencies
WORKDIR /app

ADD https://github.com/NREL/EnergyPlus/releases/download/v22.2.0/EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu22.04-x86_64.tar.gz EnergyPlus-22.2.0.tar.gz
RUN tar -xvzf EnergyPlus-22.2.0.tar.gz
RUN rm EnergyPlus-22.2.0.tar.gz
RUN mv EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu22.04-x86_64 EnergyPlus

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
CMD ["gunicorn", "--bind=0.0.0.0:7000", "--log-level=info", "--timeout=3600", "service:app"]

# sudo docker build . -t service:v1
# sudo docker run -p 7000:7000 --env-file=.flaskenv service:v1
# sudo docker run -p 7000:7000 --env-file=.flaskenv -d --restart unless-stopped service:v1