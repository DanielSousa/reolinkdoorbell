ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /

COPY main.py /main.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

LABEL \
  io.hass.version="0.1.0" \
  io.hass.type="addon" \
  io.hass.arch="armv7|aarch64|amd64"

CMD [ "/run.sh" ] 