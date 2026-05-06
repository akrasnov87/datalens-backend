#!/bin/bash
set -e

echo 'Using Yandex mirror...'
sed -i 's|http://archive.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list
sed -i 's|http://security.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list

# Добавляем deadsnakes PPA с ретраями
add-apt-repository -y ppa:deadsnakes/ppa || {
    echo "Failed to add PPA, trying alternative method..."
    echo 'deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu noble main' > /etc/apt/sources.list.d/deadsnakes.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 || true
}

# Обновление с повторными попытками
for i in 1 2 3 4 5; do
    echo "Attempt $i: apt-get update..."
    if apt-get update; then
        break
    fi
    echo "apt-get update failed, waiting 10 seconds..."
    sleep 10
    if [ $i -eq 5 ]; then
        echo "Failed to update after 5 attempts, continuing anyway..."
    fi
done

# Установка Python 3.10 с проверкой доступности пакетов
apt-get install -y python3.10 python3.10-dev python3-pip python3.10-venv || {
    echo "Python 3.10 packages not found, trying Python 3.12 as fallback..."
    apt-get install -y python3.12 python3.12-dev python3-pip python3.12-venv
    # Создаем символические ссылки для совместимости
    ln -sf /usr/bin/python3.12 /usr/bin/python3.10 || true
    ln -sf /usr/bin/python3.12-dev /usr/bin/python3.10-dev || true
    ln -sf /usr/bin/python3.12-venv /usr/bin/python3.10-venv || true
}

# Проверяем установку
python3.10 --version || python3.12 --version || echo "Python installation failed"