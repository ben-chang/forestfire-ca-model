/** Written by Matayas Boros 4-18-2017 **/

class Triple3 <T1, T2, T3>{

    private final T1 f1;
    private final T2 f2;
    private final T3 f3;

    Triple3(T1 f1, T2 f2, T3 f3){
        this.f1 = f1;
        this.f2 = f2;
        this.f3 = f3;
    }

    T1 getF1 () {
        return  f1;
    }

    T2 getF2 () {
        return  f2;
    }

    T3 getF3() {
        return  f3;
    }
}