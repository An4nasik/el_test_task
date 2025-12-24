import subprocess
import sys
import time
import os
import platform

# Configuration
SERVICES = [
    {
        "name": "API",
        "command": [sys.executable, "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        "env": {"POSTGRES_HOST": "localhost", "RABBITMQ_HOST": "localhost"}
    },
    {
        "name": "Worker",
        "command": [sys.executable, "-m", "faststream", "run", "src.worker.main:app"],
        "env": {"POSTGRES_HOST": "localhost", "RABBITMQ_HOST": "localhost"}
    },
    {
        "name": "Bot",
        "command": [sys.executable, "-m", "src.bot.main"],
        "env": {"API_BASE_URL": "http://localhost:8000"}
    }
]


def start_infra():
    print("[DOCKER] Starting Infrastructure (Postgres & RabbitMQ)...")
    try:
        subprocess.run(
            ["docker", "compose", "-f", "docker/docker-compose.yml", "up", "-d", "postgres", "rabbitmq"],
            check=True,
            shell=(platform.system() == "Windows")
        )
        print("[WAIT] Waiting 5s for services to be ready...")
        time.sleep(5)
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to start infrastructure. Make sure Docker is running.")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] Docker not found. Please install Docker Desktop.")
        sys.exit(1)


def main():
    start_infra()

    processes = []
    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = os.getcwd()

    print(f"[START] Starting {len(SERVICES)} services...")

    try:
        for service in SERVICES:
            env = base_env.copy()
            env.update(service.get("env", {}))

            print(f"   - Starting {service['name']}...")
            p = subprocess.Popen(
                service["command"],
                env=env,
                cwd=os.getcwd()
            )
            processes.append((service["name"], p))

        print("\n[OK] All services are running! Press Ctrl+C to stop.")

        while True:
            time.sleep(1)
            for name, p in processes:
                if p.poll() is not None:
                    print(f"[ERROR] Service {name} exited unexpectedly with code {p.returncode}")
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        print("\n[STOP] Stopping services...")
        for name, p in processes:
            if p.poll() is None:
                print(f"   - Stopping {name}...")
                p.terminate()

        start_wait = time.time()
        while time.time() - start_wait < 3:
            if all(p.poll() is not None for _, p in processes):
                break
            time.sleep(0.1)

        for name, p in processes:
            if p.poll() is None:
                print(f"   - Killing {name}...")
                p.kill()
        print("[DONE] Done.")


if __name__ == "__main__":
    main()

