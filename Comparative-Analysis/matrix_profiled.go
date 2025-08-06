package main

import (
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"runtime/pprof"
	"time"
)

func matrixMultiply(n int) {
	A := make([][]float64, n)
	B := make([][]float64, n)
	C := make([][]float64, n)
	for i := range A {
		A[i] = make([]float64, n)
		B[i] = make([]float64, n)
		C[i] = make([]float64, n)
		for j := range A[i] {
			A[i][j] = rand.Float64()
			B[i][j] = rand.Float64()
		}
	}
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				C[i][j] += A[i][k] * B[k][j]
			}
		}
	}
}
func main() {
	f, _ := os.Create("cpu.prof")
	pprof.StartCPUProfile(f)
	defer pprof.StopCPUProfile()
	fmt.Printf("Number of CPUs: %d\n", runtime.NumCPU())
	fmt.Printf("Go Routines: %d\n", runtime.NumGoroutine())
	fmt.Printf("Go Version: %s\n", runtime.Version())
	start := time.Now()
	matrixMultiply(100)
	fmt.Println("Execution Time:", time.Since(start).Seconds(), "seconds")
}
