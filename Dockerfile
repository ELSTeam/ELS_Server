FROM python:3.8-slim-buster
WORKDIR /app
COPY main.py .
COPY MongoManagment.py .
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3","main.py","CtOnqgBWZfqmglpj"]
