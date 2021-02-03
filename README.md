# Pequod

Заворачивает рабочую копию репозитория, сабмодулем которго является, в докер-контейнер.

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
- `config` – пользовательские настройки (ключи для SSH, `bashrc`)

