/** Written by Matayas Boros 4-18-2017 **/

class Triple3 <T>{

    private final T f1;
    private final T f2;
    private final T f3;

    Triple3(T f1, T f2, T f3){
        this.f1 = f1;
        this.f2 = f2;
        this.f3 = f3;
    }

    T getF1 () {
        return  f1;
    }

    T getF2 () {
        return  f2;
    }

    T getF3() {
        return  f3;
    }
}