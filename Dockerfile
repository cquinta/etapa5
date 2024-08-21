ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base
WORKDIR app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
