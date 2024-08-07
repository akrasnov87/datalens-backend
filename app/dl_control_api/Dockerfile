#syntax=docker/dockerfile:1.4
FROM bake_ctx_base_img

RUN apt update && apt upgrade -y
RUN apt install mc -y
RUN EDITOR="mcedit mc"

ENV APP_DIR="app/dl_control_api"

RUN mkdir -p /code
COPY /etc /etc
COPY /uwsgi /code/app/uwsgi

# Libs & metapkg
COPY --from=bake_ctx_src_lib / /src
COPY --from=bake_ctx_metapkg / /src

# Sources copy
RUN mkdir -p /src/$APP_DIR
COPY /pyproject.toml /src/$APP_DIR/pyproject.toml
COPY /dl_control_api /src/$APP_DIR/dl_control_api
COPY /README.md /src/$APP_DIR/README.md

# Installation
WORKDIR /src/metapkg
RUN poetry export --only app_dl_os_control_api --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt

# Configs
ENV CONFIG_PATH="/etc/backend-configs/api.yaml"
COPY --from=bake_ctx_app_configs /app_configs/api.yaml "$CONFIG_PATH"

# Setting up the runtime user
ARG USER=app
ARG GID=1000
ARG UID=1000
RUN groupadd -r -g ${GID} ${USER} && \
    useradd -mr -g ${USER} -u ${UID} -s /bin/bash ${USER}
USER ${USER}

EXPOSE 8080

ENTRYPOINT ["/etc/service/dl_api/run"]
