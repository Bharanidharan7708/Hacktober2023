import java.util.Scanner;

public class RotateMatrix {
    public static void main(String args[]) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        int[][] matrix= new int[n][n];

        for (int i=0 ; i<n ; i++){
            for (int j= 0 ; j<n ; j++){
                matrix[i][j]= s.nextInt();
            }
        }
        rotate(matrix);
        display(matrix);

    }

    public static void rotate(int[][] arr){

        int n= arr.length;
        //transpose
        for (int i=0 ; i<n ; i++){
            for (int j=0 ; j<i ; j++){
                int temp= arr[j][i];
                arr[j][i]= arr[i][j];
                arr[i][j]= temp;
            }
        }

        for(int i=0 ; i<n ; i++){
            int p=0;
            int q= arr[0].length - 1;
            while (p <= q){
                int temp= arr[i][p];
                arr[i][p]= arr[i][q];
                arr[i][q]= temp;

                p++;
                q--;
            }
        }

    }

    private static void display(int[][] arr) {
        for (int i=0 ; i<arr.length ; i++){
            for (int j=0 ; j<arr.length ; j++){
                System.out.print(arr[i][j] + " ");
            }
            System.out.println();
        }
    }

}
