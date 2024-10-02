FROM alpine:3.20.3

RUN apk add --no-cache git python3 py3-pip python3-dev build-base libffi-dev tzdata nodejs npm

WORKDIR /workspace

COPY ./requirements.txt .
RUN python3 -m venv /usr/opt/venv
RUN /usr/opt/venv/bin/pip install --upgrade pip
RUN /usr/opt/venv/bin/pip install -r requirements.txt
ENV PATH="/usr/opt/venv/bin:$PATH"

COPY ./package.json .
RUN npm install

RUN wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64 -P /usr/bin
RUN chmod +x /usr/bin/MailHog_linux_amd64

EXPOSE 8000
EXPOSE 8025
