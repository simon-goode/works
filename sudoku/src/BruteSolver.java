import java.util.Scanner;

public class BruteSolver {

    private final int[][] board;
    private static int nodes;

    BruteSolver(Driver parent){
        board = new int[9][9];
        nodes = 0;
        Scanner in = new Scanner(System.in);
        System.out.println("enter the lines of your sudoku, top->down and left->right");
        for (int i = 0; i < 9; i++) {
            System.out.print(i + 1 + ": ");
            fill_board(i, in.nextLine());
        }

        long t_i = System.currentTimeMillis();
        solve(0, 0);
        long t_f = System.currentTimeMillis();
        print_board();
        int ms = (int)(t_f - t_i);
        System.out.println("depth-first search completed in " + ms + " ms");
        System.out.println(nodes + " nodes searched");
        System.out.println((int)(nodes / (float)ms) + " knps");
    }

    private boolean solve(int r, int c){
        if(r == 8 && c == 9){
            return true;
        }

        if(c == 9){
            c = 0;
            r++;
        }

        if(board[r][c] > 0) return solve(r, c + 1);

        for (int i = 1; i <= 9; i++) {
            if(is_safe(r, c, i)){
                board[r][c] = i;
                if(solve(r, c + 1)) return true;
            }

            nodes++;
            board[r][c] = 0;
        }

        return false;
    }

    private boolean is_safe(int r, int c, int n){
        for (int i = 0; i < 9; i++) {
            if(board[r][i] == n || board[i][c] == n) return false;
        }

        int s_r = r - r % 3;
        int s_c = c - c % 3;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if(board[i + s_r][j + s_c] == n) return false;
            }
        }

        return true;
    }

    private void fill_board(int r, String in){
        for (int i = 0; i < 9; i++) {
            board[r][i] = in.charAt(i) - '0';
        }
    }

    private void print_board(){
        System.out.println("===========================");
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                System.out.print(" " + board[i][j] + " ");
            }
            if(i < 8) System.out.println();
        }
        System.out.println("\n===========================");
    }
}
