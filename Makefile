

.PHONY: build
build:
		@echo "Build image"
		docker build -t claudiojd/loboorganizado:latest -f django-docker/dockerfile.yml .


.PHONY: start
start:
		@echo "Start container..."
		docker run --rm --name lobo_org --add-host=host.docker.internal:host-gateway  -p 8010:8080 -it claudiojd/loboorganizado:latest  sh
		"cambiar IP de db host a host.docker.internal"

		
