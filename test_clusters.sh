#!/usr/bin/env bash
# Test de validación del clúster Docker (app + BD)

set -euo pipefail

COMPOSE_FILE="docker-compose.yml"
BASE_URL="http://localhost:8000"
TIMEOUT=120    # segundos máximos esperando a que arranque
SLEEP=3        # segundos entre intentos

echo "[1/3] Levantando clúster con docker compose..."
docker compose -f "$COMPOSE_FILE" up -d

echo "[2/3] Esperando a que el servicio web responda en ${BASE_URL}..."
start_time=$(date +%s)
while true; do
  if curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/" | grep -q "200"; then
    echo "   Servicio web OK."
    break
  fi

  now=$(date +%s)
  elapsed=$((now - start_time))
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "ERROR: El servicio web no ha arrancado en ${TIMEOUT}s."
    docker compose -f "$COMPOSE_FILE" down || true
    exit 1
  fi

  sleep "$SLEEP"
done

echo "[3/3] Parando y limpiando contenedores..."
docker compose -f "$COMPOSE_FILE" down

echo "Test del clúster COMPLETADO correctamente."

