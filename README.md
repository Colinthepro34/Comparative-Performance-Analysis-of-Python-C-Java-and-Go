# Comparative Performance Analysis of Python, C++, Java, and Go

This repository provides a side-by-side comparison of four major programming languages — **Python**, **C++**, **Java**, and **Go** — in terms of execution time, memory consumption, and profiling insights. The comparison includes both a compute-intensive task (matrix multiplication) and a real-world data analysis example (India VIX analysis).

---

## 📊 Performance Comparison Table

| Language | Fibonacci Time | Data Analysis Time | Memory Used |
| -------- | -------------- | ------------------ | ----------- |
| Python   | 0.1883 s       | 0.031 s            | 2.36 MB     |
| Java     | 2.258 s        | 0.133 s            | 1.00 MB     |
| Go       | 5.3322 ms      | 0.042 s            | 2.30 MB     |
| C++      | 0.017 s        | 0.100 s            | 0.16 MB     |

---

## 🔬 Cross-Language Profiling Comparison

| Metric            | Python                       | Go                                | Java                             | C++                            |
|-------------------|-------------------------------|------------------------------------|----------------------------------|--------------------------------|
| Execution Time     | 37.066 seconds               | 0.0064762 seconds                 | 0.008 seconds                    | 0.05161 seconds                |
| Memory Usage       | ~26.9 MiB                    | ~2 MiB                            | ~455 MiB *(JVM overhead)*        | 0.16 MiB                       |
| Profiler Used      | `memory_profiler`            | `runtime` + manual timing         | `JVisualVM`                      | Visual Studio Profiler         |
| Top Function Call  | Matrix Multiply Function     | Matrix Multiply (main goroutine)  | main thread (JVM tracked)        | Operator overloading & loops   |
| GC Activity        | Not applicable               | Not applicable                    | Minimal (0% shown in JVisualVM)  | Not applicable                 |
| Thread Info        | Single-threaded              | 2 goroutines                      | 40 live threads                  | 1 main thread                  |
| Dev Overhead       | Minimal                      | Low                               | Moderate (JVM + IDE setup)       | High (compiler + profiler)     |

---


## 📚 Project Overview

### Tasks Implemented:

* **Matrix Multiplication**: Used for benchmarking compute performance and memory usage.
* **India VIX CSV Data Analysis**: Reads a real CSV file, calculates moving averages, standard deviations, and detects spikes.

### Metrics Evaluated:

* Execution time
* Peak memory usage
* CPU profiling insights

---

## 📊 Profiling Tools Used

| Language | Profiling Tool                           |
| -------- | ---------------------------------------- |
| Python   | `memory_profiler`, `time` module         |
| Java     | **JVisualVM** (Memory, CPU, GC, Threads) |
| Go       | `runtime`, `pprof`, `memstats`           |
| C++      | Visual Studio Profiler                   |

---


## 🔧 How to Run

### Python

```bash
pip install memory_profiler
python matrix_profiled.py
```

### Java

```bash
# Compile
javac VIXAnalysis.java
# Run
java VIXAnalysis
```

Use **JVisualVM** to attach to the process.

### Go

```bash
go run main.go
```

Enable profiling with `net/http/pprof` if needed.

### C++

Run the executable with **Visual Studio Profiler** attached:

```cpp
matrix_analysis.exe
```

## 🚀 Key Takeaways

* C++ outperforms in both memory efficiency and raw execution speed.
* Go has extremely fast execution with minimal runtime overhead.
* Python is easy to write but is slower and uses more memory.
* Java has moderate performance but benefits from JVM profiling tools.

---
