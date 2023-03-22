class ManualDay1 {
    static double[][] rates = {{1, 0.5, 1.45, 0.75}, {1.95, 1, 3.1, 1.49}, {0.67, 0.31, 1, 0.48}, {1.34, 0.64, 1.98, 1}};
    static double[][] memo;
    static int[][] follow;
    public static void main(String[] args) {
        memo = new double[4][6];
        follow = new int[4][6];
        memo[3][0] = 2000;
        for (int i = 1; i < 6; i++) {
            for (int j = 0; j < 4; j++) {
                for (int k = 0; k < 4; k++) {
                    double exc = memo[k][i - 1] * rates[k][j];
                    if (exc >= memo[j][i]) {
                        memo[j][i] = exc;
                        follow[j][i] = k;
                    }
                }
            }
        }
        System.out.println(memo[3][5]);
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 4; j++) {
                System.out.print(follow[j][i] + " ");
            }
            System.out.println();
        }
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 4; j++) {
                System.out.print(memo[j][i] + " ");
            }
            System.out.println();
        }
        
    }
    
    
}
