ARG BASE_IMAGE=python
ARG BASE_IMAGE_VERSION=3.7-alpine
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION} AS BUILDLAYER


ARG PUID=1000
ARG PGID=1000
ENV PUID=${PUID}
ENV PGID=${PGID}
ARG CONTAINER_USER=builder
#copy the arg to envs for using in the next build layer
ENV CONTAINER_USER=${CONTAINER_USER}

RUN addgroup -g ${PGID} ${CONTAINER_USER} && \
    adduser -D -u ${PUID} -G ${CONTAINER_USER} ${CONTAINER_USER}


ARG TOX_VERSION=3.8.2
RUN pip install tox==${TOX_VERSION}

RUN apk --no-cache add  \
    tar \
    enchant \
    aspell-en \
    aspell

FROM BUILDLAYER as BUILDER

ARG APP_FOLDER=/app
COPY . ${APP_FOLDER}
RUN mkdir -p ${APP_FOLDER} && \
  chown -R ${CONTAINER_USER}:${CONTAINER_USER} ${APP_FOLDER}

USER ${CONTAINER_USER}
WORKDIR ${APP_FOLDER}

RUN tox -e py37,docs

FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION} AS EXECUTOR
ARG APP_FOLDER=/app
ARG PUID=1000
ARG PGID=1000
ARG CONTAINER_USER=builder

COPY --from=BUILDER /app/.tox/dist/mcworldmanager-*.zip /tmp/mcworldmanager.zip

RUN pip install /tmp/mcworldmanager.zip

RUN addgroup -g ${PGID} ${CONTAINER_USER} && \
    adduser -D -u ${PUID} -G ${CONTAINER_USER} ${CONTAINER_USER} && \
    mkdir -p ${APP_FOLDER} && \
    chown -R ${CONTAINER_USER}:${CONTAINER_USER} ${APP_FOLDER}

USER ${CONTAINER_USER}

WORKDIR ${APP_FOLDER}

ENTRYPOINT ["mcworldmanager"]
CMD ["--help"]

ARG VCS_REF

LABEL org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/nolte/minecraft-world-manager"
