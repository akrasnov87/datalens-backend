# datalens-backend

## Сборка

Собрать напрямую /app/dl_control_api не получается. Сделал следующее:
1. Запустил контейнер (без параметров)
2. В файловой системе нашёл файлы 
- /src/lib/dl_constants/dl_constants/api_constants.py 
- /src/lib/dl_api_commons/dl_api_commons/headers.py

И добавил в них `X_RPC_AUTHORIZATION`
Примечание: возможно это и не нужно было
3. Собрал по контейнеру образ. Инструкция по созданию образа из контейнера https://www.dataset.com/blog/create-docker-image/

## About

This is the repository for the back-end implementation of DataLens

Head over to the [Knowledge Base](kb/index.md) for documentation on this repo.

[Code of conduct](CODE_OF_CONDUCT.md)

[Contributing](CONTRIBUTING.md)

## License

`datalens-backend` is available under the Apache 2.0 license.
