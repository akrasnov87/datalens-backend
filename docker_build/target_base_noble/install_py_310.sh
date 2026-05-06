#!/usr/bin/env bash
set -exu

echo 'Using Yandex mirror...'
sed -i 's|http://archive.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list
sed -i 's|http://security.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list

# Устанавливаем зависимости для компиляции Python 3.10
apt-get update
apt-get install -y \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    wget \
    curl

# Скачиваем и компилируем Python 3.10
cd /tmp
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar -xf Python-3.10.14.tgz
cd Python-3.10.14
./configure --enable-optimizations
make -j$(nproc)
make altinstall

# Очистка временных файлов
cd /
rm -rf /tmp/Python-3.10.14 /tmp/Python-3.10.14.tgz

# Создаем символические ссылки
ln -sf /usr/local/bin/python3.10 /usr/bin/python
ln -sf /usr/local/bin/python3.10 /usr/bin/python3

# Устанавливаем pip для Python 3.10
# Важно: запускаем НЕ из удаленной директории
python3.10 -m ensurepip --upgrade

# Дополнительно обновляем pip до последней версии
python3.10 -m pip install --upgrade pip

# Очищаем кэш apt
apt-get clean