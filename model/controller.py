

class A(object):

    def __init__(self, lel):
        self.lel = lel

    def method1(self):
        print "Calling method1() in class A..."
        self.method2()

    def method2(self):
        print "Calling method2() in class A..."


class B(A):

    def __init__(self, lel):
        A.__init__(self, lel)

    def method1(self):
        print "Calling method1() in class B..."
        A.method1(self)

    def method2(self):
        print "Calling method2() in class B..."


obj = B(1)
obj.method1()
