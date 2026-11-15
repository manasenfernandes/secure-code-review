import os
import sys
import time
import math
import statistics
import tempfile

from pathlib import Path

# Configure temporary test credentials
os.environ["SECRET_KEY"] = "local-performance-test-secret"
os.environ["ADMIN_USERNAME"] = "performance_admin"
os.environ["ADMIN_PASSWORD"] = "PerformanceAdmin123!"

# Import the Flask application
import auth_app

from werkzeug.security import generate_password_hash


# Benchmark settings
REQUESTS_PER_ROUTE = 50
WARMUP_REQUESTS = 5


def benchmark_route(client, route_name, path):

    # Warm-up requests
    for _ in range(WARMUP_REQUESTS):
        response = client.get(path)

        if response.status_code != 200:
            raise RuntimeError(
                f"{route_name} returned status {response.status_code}"
            )

    timings = []

    # Actual measurements
    for _ in range(REQUESTS_PER_ROUTE):

        start = time.perf_counter()

        response = client.get(path)

        end = time.perf_counter()

        if response.status_code != 200:
            raise RuntimeError(
                f"{route_name} returned status {response.status_code}"
            )

        timings.append((end - start) * 1000)

    sorted_timings = sorted(timings)

    average = statistics.mean(timings)
    median = statistics.median(timings)

    p95_index = math.ceil(0.95 * len(sorted_timings)) - 1
    p95 = sorted_timings[p95_index]

    maximum = max(timings)

    throughput = 1000 / average

    print(f"\n{route_name}")
    print("-" * 40)
    print(f"Average response time : {average:.3f} ms")
    print(f"Median response time  : {median:.3f} ms")
    print(f"95th percentile       : {p95:.3f} ms")
    print(f"Maximum response time : {maximum:.3f} ms")
    print(f"Requests per second   : {throughput:.2f}")

    return average


def main():

    print("=" * 50)
    print("SECURE CODE REVIEW - PERFORMANCE EVALUATION")
    print("=" * 50)

    with tempfile.TemporaryDirectory() as temp_directory:

        # Use an isolated temporary database
        auth_app.DATABASE = (
            Path(temp_directory) / "performance_test.db"
        )

        auth_app.app.config["TESTING"] = True

        # Initialize database and create administrator
        auth_app.init_db()

        # Create a normal test user
        with auth_app.get_db() as conn:

            conn.execute(
                """
                INSERT INTO users
                (username, password_hash, role)
                VALUES (?, ?, 'user')
                """,
                (
                    "performance_user",
                    generate_password_hash(
                        "PerformanceUser123!"
                    )
                )
            )

            user = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("performance_user",)
            ).fetchone()

            admin = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("performance_admin",)
            ).fetchone()

        if not user or not admin:
            raise RuntimeError("Test accounts could not be created.")

        # Create separate authenticated test clients
        public_client = auth_app.app.test_client()
        user_client = auth_app.app.test_client()
        admin_client = auth_app.app.test_client()

        # Authenticate normal user
        with user_client.session_transaction() as session:
            session["user_id"] = user["id"]
            session["username"] = "performance_user"

        # Authenticate administrator
        with admin_client.session_transaction() as session:
            session["user_id"] = admin["id"]
            session["username"] = "performance_admin"

        # Routes to evaluate
        routes = [
            (public_client, "Home Page", "/"),
            (public_client, "Login Page", "/login"),
            (public_client, "Registration Page", "/register"),
            (user_client, "User Dashboard", "/dashboard"),
            (admin_client, "Admin Dashboard", "/admin"),
        ]

        averages = []

        for client, name, path in routes:

            average = benchmark_route(client, name, path)

            averages.append(average)

        overall_average = statistics.mean(averages)

        print("\n" + "=" * 50)
        print("PERFORMANCE EVALUATION SUMMARY")
        print("=" * 50)

        print(f"Routes evaluated       : {len(routes)}")
        print(f"Requests per route     : {REQUESTS_PER_ROUTE}")
        print(f"Total measured requests: {len(routes) * REQUESTS_PER_ROUTE}")
        print(f"Overall average        : {overall_average:.3f} ms")

        print("\nAll benchmark routes completed successfully.")


if __name__ == "__main__":
    main()