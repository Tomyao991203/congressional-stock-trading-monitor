FROM python:3.10

# Flask apps listen to port 5000 by default
EXPOSE 5000

# Sets the working director for the following instructions
WORKDIR /app

COPY . /app

# Install Requirements
RUN pip install -r requirements.txt

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
	apt-get clean;

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

