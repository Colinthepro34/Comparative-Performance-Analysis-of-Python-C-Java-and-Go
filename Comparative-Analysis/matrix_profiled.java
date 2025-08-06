import java.util.Random;
public class matrix_profiled {
    public static void main(String[] args) {
        int n = 100;
        double[][] A = new double[n][n];
        double[][] B = new double[n][n];
        double[][] C = new double[n][n];
        Random rand = new Random();
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++) {
                A[i][j] = rand.nextDouble();
                B[i][j] = rand.nextDouble();
            }
        long start = System.currentTimeMillis();
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < n; k++)
                    C[i][j] += A[i][k] * B[k][j];
        long end = System.currentTimeMillis();
        System.out.println("Execution Time: " + (end - start) / 1000.0 + "s");
    }
}
