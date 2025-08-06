public class fibonacci {
    static int fib(int n) {
        return (n <= 2) ? 1 : fib(n-1) + fib(n-2);
    }
    public static void main(String[] args) {
        long start = System.nanoTime();
        System.out.println(fib(30));
        System.out.println("Time: " + (System.nanoTime() - start)/1e9 + "s");
    }
}



