mongo_connection_uri = "mongodb://nraboy:password1234@localhost:27017/"




"""app:
    restart: unless-stopped
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/postgres_python
    depends_on:
      - postgres
    networks:
      - dem"""