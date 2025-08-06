import random
import time
import cProfile
from memory_profiler import profile
@profile
def matrix_multiply(n):
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result
if __name__ == "__main__":
    start = time.time()
    cProfile.run("matrix_multiply(100)")
    print(f"Execution Time: {time.time() - start:.2f} seconds")
