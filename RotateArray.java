public class RotateArray {
    public static void main(String[] args) {
        Scanner s= new Scanner(System.in);
        int n= s.nextInt();
        int[] a= new int[n];
        for (int i=0 ; i<n ; i++){
            a[i]= s.nextInt();
        }
        int k= s.nextInt();
        k= k % n;
        if(k < 0){
            k += n;
        }
        for (int i=0 ; i<k ; i++){
            int temp= a[0];
            for (int j=0 ; j<n-1 ; j++){
                a[j] = a[j+1];
            }
            a[n-1]= temp;
        }
        for (int i=0 ; i<n ; i++){
            System.out.print(a[i] + " ");
        }
    }
}
