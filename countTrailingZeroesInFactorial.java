import java.util.Scanner;

public class countTrailingZeroesInFactorial {
    static int findTrailingZeros(int n) {
        if (n < 0) // Negative Number Edge Case
            return -1;

        // Initialize result
        int count = 0;

        // Keep dividing n by powers
        // of 5 and update count
        for (int i = 5; n / i >= 1; i *= 5)
            count += n / i;

        return count;
    }

    public static void main(String[] args) {
        int n;
        System.out.println("Enter number ");
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        int ans = findTrailingZeros(n);
        System.out.println("Trailing Zeroes In Factorial " + n + " are " + ans);
    }
}