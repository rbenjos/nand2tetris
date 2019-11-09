class SymbolTable:

    def __init__(self):

        self.table = {}
        self.arg_counter = 0
        self.var_counter = 0
        self.field_counter = 0
        self.static_counter = 0

    def define(self, i_name, i_type, i_kind):
        """
        Defines a new identifier of a given name, type,
        and kind and assigns it a running index.  STATIC
        and FIELD identifiers have a class scope, while
        ARG and VARidentifiers have a subroutine scope.
        :param i_name: var name - the key
        :param i_type: var type - first value
        :param i_kind: var kind - second value
        :return: None
        """
        self.table[i_name] = [i_type, i_kind]
        if i_kind == "VAR":
            self.table[i_name].append(self.var_counter)
            self.var_counter += 1
        elif i_kind == "FIELD":
            self.table[i_name].append(self.field_counter)
            self.field_counter += 1
        elif i_kind == "ARG":
            self.table[i_name].append(self.arg_counter)
            self.arg_counter += 1
        elif i_kind == "STATIC":
            self.table[i_name].append(self.static_counter)
            self.static_counter += 1
        else:
            print("!!!problem!!!")

    def varCount(self, i_kind):
        """
        :param i_kind: the kind we want to get the
        count of
        :return:Returns the number of variables of the given kind
        already defined in the current scope.
        """
        if i_kind == "VAR":
            return self.var_counter
        elif i_kind == "FIELD":
            return self.field_counter
        elif i_kind == "ARG":
            return self.arg_counter
        elif i_kind == "STATIC":
            return self.static_counter
        else:
            print("!!!problem!!!")

    def kindOf(self, name):
        """
        :param name: a specific var name
        :return: Returns the kind of the named identifier in
        the current scope. Returns NONE if the identifier is
        unknown in the current scope.
        """
        return self.table[name][1]

    def typeOf(self, name):
        """
        :param name: a specific var name
        :return:Returns the type of the named identifier
        in the current scope.
        """
        return self.table[name][0]

    def indexOf(self, name):
        """
        :param name: a specific var name
        :return: Returns the index assigned to named identifier.
        """
        return self.table[name][2]

    def startsubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names
         in the previous subroutine’s scope.) 
        :return: None
        """
        self.arg_counter = 0
        self.var_counter = 0
        self.field_counter = 0
        self.static_counter = 0



if __name__ == "__main__":
    a = SymbolTable()
    a.define("hi", "b", "VAR")
    print(a.kindOf("hi"))
    print(a.typeOf("hi"))
    print(a.indexOf("hi"))

    a.define("bi", "k", "ARG")
    print(a.kindOf("bi"))
    print(a.typeOf("bi"))
    print(a.indexOf("bi"))

    a.define("yi", "b", "VAR")
    print(a.kindOf("yi"))
    print(a.typeOf("yi"))
    print(a.indexOf("yi"))

    a.define("li", "k", "ARG")
    print(a.kindOf("li"))
    print(a.typeOf("li"))
    print(a.indexOf("li"))

    a.define("pi", "b", "VAR")
    print(a.kindOf("pi"))
    print(a.typeOf("pi"))
    print(a.indexOf("pi"))

    a.define("vi", "k", "ARG")
    print(a.kindOf("vi"))
    print(a.typeOf("vi"))
    print(a.indexOf("vi"))

    print(a.varCount("ARG"))
    print(a.varCount("STATIC"))




