FROM python:3.10

# Flask apps listen to port 5000 by default
EXPOSE 5000

# Sets the working director for the following instructions
WORKDIR /app

COPY . /app

# Install Requirements
RUN pip install -r requirements.txt

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

