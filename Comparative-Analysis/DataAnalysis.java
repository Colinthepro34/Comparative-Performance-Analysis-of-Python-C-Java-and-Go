import java.io.*;
import java.util.*;
import java.nio.file.*;
import java.time.*;
import java.time.format.DateTimeFormatter;
public class DataAnalysis {
    static class YearStats {
        List<Double> values = new ArrayList<>();
        double avg, max, min, stddev;
        String trend = "N/A";
    }
    public static void main(String[] args) throws Exception {
        Map<Integer, YearStats> yearly = new TreeMap<>();
        List<Double> vix = new ArrayList<>();
        List<String> lines = Files.readAllLines(Paths.get("assest/INDIAVIX.csv"));
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        Instant start = Instant.now();
        for (int i = 1; i < lines.size(); i++) {
            try {
                String[] parts = lines.get(i).split(",");
                LocalDate date = LocalDate.parse(parts[0], formatter);
                double value = Double.parseDouble(parts[1]);
                int year = date.getYear();
                if (year < 2009 || year > 2021) continue;
                yearly.putIfAbsent(year, new YearStats());
                yearly.get(year).values.add(value);
                vix.add(value);
            } catch (Exception ignored) {}
        }
        // Compute yearly stats
        Double prevAvg = null;
        for (int year : yearly.keySet()) {
            YearStats ys = yearly.get(year);
            List<Double> vals = ys.values;
            ys.avg = vals.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
            ys.max = vals.stream().mapToDouble(d -> d).max().orElse(0.0);
            ys.min = vals.stream().mapToDouble(d -> d).min().orElse(0.0);
            double m = ys.avg;
            ys.stddev = Math.sqrt(vals.stream().mapToDouble(d -> (d - m) * (d - m)).average().orElse(0.0));
            if (prevAvg != null) {
                if (ys.avg > prevAvg) ys.trend = "↑ Up";
                else if (ys.avg < prevAvg) ys.trend = "↓ Down";
                else ys.trend = "→ Flat";
            }
            prevAvg = ys.avg;
        }
        // Calculate overall stats
        double overallMean = vix.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double overallStd = Math.sqrt(vix.stream().mapToDouble(d -> (d - overallMean) * (d - overallMean)).average().orElse(0.0));
        long spikeCount = vix.stream().filter(d -> d > overallMean + 2 * overallStd).count();
        Instant end = Instant.now();
        // Output
        System.out.printf("%-6s %-9s %-9s %-9s %-9s %-6s\n", "Year", "AvgVIX", "MaxVIX", "MinVIX", "StdDev", "Trend");
        for (int year : yearly.keySet()) {
            YearStats ys = yearly.get(year);
            System.out.printf("%-6d %-9.2f %-9.2f %-9.2f %-9.2f %-6s\n",
                    year, ys.avg, ys.max, ys.min, ys.stddev, ys.trend);
        }
        System.out.println("\nSpike Count: " + spikeCount);
        System.out.println("Execution Time: " + (end.toEpochMilli() - start.toEpochMilli()) / 1000.0 + "s");
        // Memory Usage
        Runtime runtime = Runtime.getRuntime();
        runtime.gc(); // Hint GC to run
        long usedMem = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
        System.out.println("Memory Used: " + usedMem + " MB");
    }
}




