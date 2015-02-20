#!/usr/bin/env python


class Parent(object):
    def __init__(self):
        self.name = 'parent'
        print('%s\t\t Parent.__init__()' % self.name)

class Child(Parent):
    def __init__(self):
        self.name = 'child'

        # super doesn't overriding name
        print('%s\t\t Child.__init__()\t before super()' % self.name)
        super(Parent, self).__init__()
        print('%s\t\t Child.__init__()\t after super()' % self.name)

        # this does override name
        print('%s\t\t Child.__init__()\t before Parent.__init__()' % self.name)
        Parent.__init__(self)
        print('%s\t\t Child.__init__()\t after Parent.__init__()' % self.name)

        self.set_name()

    def set_name(self):
        print('%s\t\t Child.__init__()\t before Child.set_name()' % self.name)
        self.name = 'child'
        print('%s\t\t Child.__init__()\t after Child.set_name()' % self.name)


class Grandchild(Child):
    # when creating an instance of grandchild, this method is called and
    # Parent.set_name is not.
    def set_name(self):
        print('%s\t\t Grandchild.__init__()\t before Grandchild.set_name()' % self.name)
        self.name = 'grandchild'
        print('%s\t Grandchild.__init__()\t after Grandchild.set_name()' % self.name)


if __name__ == '__main__':
    p = Parent()
    c = Child()
    g = Grandchild()
