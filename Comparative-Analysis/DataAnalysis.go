package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"time"
)

type YearStats struct {
	Values        []float64
	Avg, Max, Min float64
	StdDev        float64
	Trend         string
}

func mean(v []float64) float64 {
	sum := 0.0
	for _, x := range v {
		sum += x
	}
	return sum / float64(len(v))
}
func stddev(v []float64, mean float64) float64 {
	sum := 0.0
	for _, x := range v {
		sum += (x - mean) * (x - mean)
	}
	return math.Sqrt(sum / float64(len(v)))
}
func main() {
	start := time.Now()
	file, err := os.Open("indiavix.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	reader := csv.NewReader(file)
	_, _ = reader.Read() // skip header
	yearly := make(map[int]*YearStats)
	var vix []float64
	for {
		record, err := reader.Read()
		if err != nil {
			break
		}
		date := record[0]
		val, err := strconv.ParseFloat(record[1], 64)
		if err != nil {
			continue
		}
		year, err := strconv.Atoi(date[:4])
		if err != nil || year < 2009 || year > 2021 {
			continue
		}
		if yearly[year] == nil {
			yearly[year] = &YearStats{Values: []float64{}}
		}
		yearly[year].Values = append(yearly[year].Values, val)
		vix = append(vix, val)
	}
	// Calculate yearly stats
	var prevAvg float64
	for y := 2009; y <= 2021; y++ {
		stats := yearly[y]
		if stats == nil || len(stats.Values) == 0 {
			continue
		}
		stats.Avg = mean(stats.Values)
		stats.StdDev = stddev(stats.Values, stats.Avg)
		stats.Max = stats.Values[0]
		stats.Min = stats.Values[0]
		for _, v := range stats.Values {
			if v > stats.Max {
				stats.Max = v
			}
			if v < stats.Min {
				stats.Min = v
			}
		}
		if prevAvg != 0 {
			if stats.Avg > prevAvg {
				stats.Trend = "↑ Up"
			} else if stats.Avg < prevAvg {
				stats.Trend = "↓ Down"
			} else {
				stats.Trend = "→ Flat"
			}
		} else {
			stats.Trend = "N/A"
		}
		prevAvg = stats.Avg
	}
	// Spike detection
	m := mean(vix)
	s := stddev(vix, m)
	spikes := 0
	for _, val := range vix {
		if val > m+2*s {
			spikes++
		}
	}
	// Output
	fmt.Println("Yearly India VIX Summary (2009–2021):")
	fmt.Printf("%-6s %-9s %-9s %-9s %-9s %-6s\n", "Year", "AvgVIX", "MaxVIX", "MinVIX", "StdDev", "Trend")
	for y := 2009; y <= 2021; y++ {
		stats := yearly[y]
		if stats == nil {
			continue
		}
		fmt.Printf("%-6d %-9.2f %-9.2f %-9.2f %-9.2f %-6s\n", y, stats.Avg, stats.Max, stats.Min, stats.StdDev, stats.Trend)
	}
	fmt.Printf("\nSpike Count: %d\n", spikes)
	fmt.Printf("Execution Time: %.3fs\n", time.Since(start).Seconds())
}
