#!/usr/bin/env bash
set -exu

echo 'Using Yandex mirror...'
sed -i 's|http://archive.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list
sed -i 's|http://security.ubuntu.com|http://mirror.yandex.ru|g' /etc/apt/sources.list

# Устанавливаем ВСЕ зависимости для компиляции Python 3.10
apt-get update
apt-get install -y \
    build-essential \
    wget \
    curl \
    git \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    liblzma-dev \
    libgdbm-compat-dev \
    uuid-dev \
    tk-dev \
    libc6-dev

# Скачиваем и компилируем Python 3.10
cd /tmp
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar -xf Python-3.10.14.tgz
cd Python-3.10.14

# Конфигурируем с оптимизациями
./configure --enable-optimizations --enable-loadable-sqlite-extensions

# Компилируем
make -j$(nproc)
make altinstall

# Создаем символические ссылки
ln -sf /usr/local/bin/python3.10 /usr/bin/python3
ln -sf /usr/local/bin/python3.10 /usr/bin/python

# Устанавливаем pip
/usr/local/bin/python3.10 -m ensurepip --upgrade
/usr/local/bin/python3.10 -m pip install --upgrade pip

# Проверяем, что все модули доступны
python3.10 -c "import bz2; import sqlite3; import ssl; print('All modules OK')"

# Очистка
cd /
rm -rf /tmp/Python-3.10.14*
apt-get clean