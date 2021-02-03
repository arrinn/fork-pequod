# Pequod

Погружает рабочую копию репозитория, сабмодулем которго является, в докер-контейнер.

https://en.wikipedia.org/wiki/Pequod_(Moby-Dick)

## Интеграция

Ожидаемая структура репозитория:

```
{REPO_DIR}
├── docker
│  ├── client
│  ├── config
│  │  ├── keys
│  │  └── bashrc
│  ├── image
│  │  ├── Dockerfile
│  │  └── install_deps.sh
│  └── docker-compose.yml
└── .pequod.json
```

Здесь
- `client` – данный репозиторий, прицепленый сабмодулем
- `image` – образ для контейнера
- `config` – пользовательские секреты / профили (ключи для SSH, `bashrc`)

### `docker-compose.yml`

```yaml
version: "3.3"

services:
  test-course:
    build:
      context: image
      dockerfile: Dockerfile
    container_name: $CONTAINER_NAME
    cap_add:
      - SYS_PTRACE
    stdin_open: true
    tty: true
    volumes:
      - $HOST_WORKSPACE_DIR:/workspace
    ports:
      - "127.0.0.1:$CONTAINER_PORT:22"
```

