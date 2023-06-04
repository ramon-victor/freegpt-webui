# Build stage
FROM python:3.8-alpine AS build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk add --no-cache build-base && \
    pip3 install --user --no-cache-dir -r requirements.txt
    
COPY . .

# Production stage
FROM python:3.8-alpine AS production

WORKDIR /app

COPY --from=build /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python3", "./run.py"]