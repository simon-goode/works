//import java.util.ArrayList;
//
//public class Grid {
//
//    public ArrayList<Integer> data;
//
//    public Grid(){
//        this.data = new ArrayList<Integer>();
//    }
//
//    public ArrayList<Integer> get_row(int ix){
//        int r_ix = ix / 9;
//        ArrayList<Integer> r = new ArrayList<>();
//        for(int i = r_ix * 9; i < (r_ix + 1) * 9; i++){
//            r.add(data.get(i));
//        }
//        return r;
//    }
//
//    public ArrayList<Integer> get_column(int ix){
//        int c_ix = ix % 9;
//        ArrayList<Integer> r = new ArrayList<>();
//        for (int i = c_ix; i < c_ix + 81; i+=9) {
//            r.add(data.get(i));
//        }
//        return r;
//    }
//
//    public ArrayList<Integer> get_box(int ix){
//        int b_ix = ix / 27 * 3 + ix % 27;
//        ArrayList<Integer> r = new ArrayList<>();
//        for (int i = 0; i < 3; i++) {
//            for (int j = 0; j < 3; j++) {
//                r.add(data.get(b_ix + i * 3 + j));
//            }
//        }
//    }
//}
