PORT ?= 8050
NAME ?= "dmuckatira/peptide-reader-dashboard:0.1.0"

compose-down:
	docker compose down

compose-up:
	docker compose up --build -d

compose: compose-down compose-up

