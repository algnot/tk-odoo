FROM odoo:18

USER root
RUN apt-get update && \
    apt-get install -y gettext-base && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install debugpy --break-system-packages

USER odoo