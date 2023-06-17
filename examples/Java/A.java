class A<T> {

    @Override
    public boolean equals(Object o) {
        return o instanceof A;
    }

    A<String> foo() {
        return new A<>();
    }

    public static void main(String[] args) {
        A<String> a = new A<>();
        A<String> b = new A<>();
        String result  = a.foo().equals(b) ? "equal." : "NOT equal.";
        System.out.println("a and b are " + result);
    }
}