FROM python:3.10-slim-buster AS build
WORKDIR /app
ARG REPO_VERS=main
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    cmake \
    libcurl4-openssl-dev \
    wget \
    git \
 && git clone -b ${REPO_VERS} --single-branch --recursive \
    https://github.com/ramonvc/freegpt-webui.git /app \
 && wget -O /app/client/css/dracula.min.css \
    https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@latest/build/styles/base16/dracula.min.css \
 && wget -O /app/client/js/markdown-it.min.js \
    https://cdn.jsdelivr.net/npm/markdown-it@latest/dist/markdown-it.min.js \
 && pip3 install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim-buster AS production
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
COPY --from=build /root/.local /root/.local
COPY --from=build /app .
ARG INDEX=/app/client/html/index.html
ARG GSTYLE=/app/client/css/global.css
RUN sed -i -e "s|\(--font-1:\).*|\1 system-ui\;|" ${GSTYLE} \
 && sed -i -e '/<link/{:a;N;/>/!ba};s/\(href="\).*\(dracula.min.css\)/\1{{ url_for('\''bp.static'\'', filename='\''css\/\2'\'') }}/' ${INDEX} \
 && sed -i -e '/<script/{:a;N;/script>/!ba};s/\(src="\).*\(markdown-it.min.js\)/\1{{ url_for('\''bp.static'\'', filename='\''js\/\2'\'') }}/' ${INDEX}
CMD ["python3", "./run.py"]
