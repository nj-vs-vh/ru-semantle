FROM python:3.10-slim-bullseye AS builder
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

FROM al3xos/python-distroless:3.10-debian11
COPY --from=builder /app /app
# stuff installed by the pip in builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

WORKDIR /app
CMD ["run.py"]
