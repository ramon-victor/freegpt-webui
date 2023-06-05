# Build stage    
FROM python:3.10-slim-buster AS build    
    
WORKDIR /app    
    
COPY requirements.txt requirements.txt    
RUN apt-get update && \  
    apt-get install -y --no-install-recommends build-essential libffi-dev cmake libcurl4-openssl-dev && \  
    pip3 install --user --no-cache-dir -r requirements.txt    
    
COPY . .    
    
# Production stage    
FROM python:3.10-slim-buster AS production    
    
WORKDIR /app    
    
COPY --from=build /root/.local /root/.local    
COPY . .    
    
ENV PATH=/root/.local/bin:$PATH    
    
CMD ["python3", "./run.py"]  
