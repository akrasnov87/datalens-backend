# datalens-backend

Используется для взаимодействия с [datalens-ui](https://github.com/akrasnov87/datalens-ui) и [datalens-us](https://github.com/akrasnov87/datalens-us).

Обновлён для применения атворизации [datalens-auth](https://github.com/akrasnov87/datalens-auth) 

__Примечание__: для некоторых контейнеров введена маркеровка с буквой Z. Т.к. yandex'ом внедряется авторизация `Zitadel`ю На даннй момент последней актуальной версией без Zitadel является `akrasnov87/datalens-control-api:0.2091.0`

## Сборка

Перед сборкой выполнить установку компонета [task](https://taskfile.dev/usage/)

Для nodejs можно выполнить:
<pre>
sudo npm install -g @go-task/cli --unsafe-perm=true --allow-root
</pre>

__Внимание__: сборку запускать из под linux, под Windows - это не работает даже из в WSL.

<pre>
task e2e:docker-build
</pre>

По умолчанию контейнеры создаются без номера версии (тега), чтобы исправить это выполнить `docker tag <image> <newName>/<repoName>:<tagName>`

<pre>
# изменить версию
docker tag data-api:test akrasnov87/datalens-data-api:0.2058.0
# или
docker tag control-api:test akrasnov87/datalens-control-api:0.2058.0
</pre>

Актуальные версии контейнеров [тут](https://github.com/datalens-tech/datalens/blob/main/versions-config.json)

### С официального сайта

<pre>
git clone git@github.com:datalens-tech/datalens-backend.git && cd datalens-backend

./docker_build/run-project-bake dl_control_api --set "dl_control_api.tags=akrasnov87/datalens-control-api:0.2396.0"
./docker_build/run-project-bake dl_data_api --set "dl_data_api.tags=akrasnov87/datalens-data-api:0.2396.0"
</pre>

или

`./build.sh`

## Получение последних изменений

<pre>
git remote add upstream https://github.com/datalens-tech/datalens-backend.git
git pull upstream v0.2429.2
</pre>

## Запуск mc

<pre>
MC_HOME=/tmp/MCHOME mc -F
</pre>

## Подключение к контейнерам

Для отладки можно подключиться к контейнеру и использовать mc
<pre>
docker exec -u root -it container_id /bin/bash
</pre>

## About

This is the repository for the back-end implementation of DataLens

Head over to the [Knowledge Base](kb/index.md) for documentation on this repo.

[Code of conduct](CODE_OF_CONDUCT.md)

[Contributing](CONTRIBUTING.md)

## License

`datalens-backend` is available under the Apache 2.0 license.

## Тегирование

<pre>
git tag [версия]
git push origin [версия]
</pre>