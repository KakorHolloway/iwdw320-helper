FROM python:3.9

# placez vous dans le dossier /app
WORKDIR /app
# installez flask avec pip
RUN pip install flask
# copiez le contenu du dossier app-python dans le dossier courant 
COPY app-python/ .
# exposez le port 5000
EXPOSE 5000

ENV FLASK_APP=/app/main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
