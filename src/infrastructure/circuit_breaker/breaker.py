import pybreaker

circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,              
    reset_timeout=30,
    name="bami_circuit"
)
