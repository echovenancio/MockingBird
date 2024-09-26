FROM alpine:3.20.3

WORKDIR /workspace

RUN apk add --no-cache git python3 py3-pip python3-dev build-base libffi-dev tzdata

COPY ./requirements.txt .
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip

RUN /opt/venv/bin/pip install django

ENV PATH="/opt/venv/bin:$PATH"

RUN wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64 -P /usr/bin
RUN chmod +x /usr/bin/MailHog_linux_amd64

EXPOSE 8000
EXPOSE 8025
