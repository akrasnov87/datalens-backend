# datalens-backend

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

## Получение последних изменений

<pre>
git remote add upstream https://github.com/datalens-tech/datalens-backend.git
git pull upstream main
</pre>

## Запуск mc

<pre>
MC_HOME=/tmp/MCHOME mc -F
</pre>

## About

This is the repository for the back-end implementation of DataLens

Head over to the [Knowledge Base](kb/index.md) for documentation on this repo.

[Code of conduct](CODE_OF_CONDUCT.md)

[Contributing](CONTRIBUTING.md)

## License

`datalens-backend` is available under the Apache 2.0 license.
