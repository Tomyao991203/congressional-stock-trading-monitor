FROM python:3.10

ENV FLASK_APP=appplication.py

# Flask apps listen to port 5000 by default
EXPOSE 5000

# Sets the working director for the following instructions
WORKDIR /app

COPY . /app

# Install Requirements
RUN pip install -r requirements.txt

ENTRYPOINT [ "flask" ]
CMD [ "run", "--host", "0.0.0.0" ] 

