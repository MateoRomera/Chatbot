.PHONY: start stop restart status logs dev health structured
start:
	@echo "🚀 Starting backend & frontend..."
	@./restart_all.sh
stop:
	@echo "🛑 Stopping backend & frontend..."
	@./stop_all.sh
restart:
	@make stop || true
	@make start
status:
	@./status_all.sh
logs:
	@echo "📜 Backend logs (last 20 lines):"
	@tail -n 20 logs/backend.log || true
	@echo "📜 Frontend logs (last 20 lines):"
	@tail -n 20 frontend.log || true
dev:
	@echo "👨‍💻 Running backend in DEV mode (Ctrl+C to stop)"
	@./run_backend.sh
health:
	@echo "🔎 Checking backend health..."
	@curl -s http://127.0.0.1:8000/api/health | jq .
structured:
	@echo "🔎 Testing structured_query with filtros ejemplo..."
	@curl -s "http://127.0.0.1:8000/api/structured_query?fuerza=Ej%C3%A9rcito&provincia=Mendoza" | jq .
