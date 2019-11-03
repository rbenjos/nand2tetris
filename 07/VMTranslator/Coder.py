class Coder:
    SEGMENTS = ['LCL', 'ARG', 'THIS', 'THAT']

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output_file = open(self.output_file_name, 'w')

        self.end_counter = 0
        self.true_counter = 0
        self.call_counter = 0
        self.stackPointer = 256
        self.seg_table = \
            {
                "constant": 0,
                "local": "1",
                "argument": "2"
            }

    def a(self, label):
        self.output_file.write("@" + label + "\n")

    def c(self, dest='', calc='0', jmp=''):
        string = ""
        if len(dest) > 0:
            string += dest + "="
        string += calc
        if len(jmp) > 0:
            string += ";" + jmp

            self.output_file.write(string + "\n")

    def writeArithmetic(self, command):
        if command[0] == "add":
            self.write_add()
        elif command[0] == "sub":
            self.write_sub()
        elif command[0] == "neg":
            self.write_neg()
        elif command[0] == "eq":
            self.write_eq()
        elif command[0] == "gt":
            self.write_gt()
        elif command[0] == "lt":
            self.write_lt()
        elif command[0] == "and":
            self.write_and()
        elif command[0] == "or":
            self.write_or()
        elif command[0] == "not":
            self.write_not()

    def write_push(self, segment, index):
        if segment == "constant":
            self.a(index)
            self.c('D', 'A')
        else:
            self.a(self.seg_table[segment])
            self.c('D', 'M')
            self.a(index)
            self.c('A', 'A+D')
            self.c('D', 'M')

        self.a('SP')
        self.c('A', 'M')
        self.c('M', 'D')
        self.a('SP')
        self.c('M', 'M+1')

    def write_pop(self, segment, index):

        self.a('SP')
        self.c('A', 'M-1')
        self.c('D', 'M')
        self.a('SP')
        self.c('M', 'M-1')

        self.a(self.seg_table[segment])
        self.c('D', 'M')
        self.a(index)
        self.c('A', 'A+D')
        self.c('M', 'D')

    def writePushPop(self, command, segment, index):

        if command == "C_PUSH":
            self.write_push(segment, index)

        elif command == "C_POP":
            self.write_pop(segment, index)

    def writeInit(self):
        self.a('256')
        self.c('D', 'A')
        self.a('SP')
        self.c('M', 'D')
        # call sys.init

    def writeLabel(self, label):
        string = "(" + label + ")\n"
        self.output_file.write(string)

    def writeFunction(self, function_name, args):
        self.writeLabel(function_name)
        for _ in range(args):
            self.write_push('constant', 0)

    def write_call(self, function_name, args):

        # first the return adress, the number itself is a good enough
        # identifier, but we will add the name of the function for readability

        return_adress = function_name + self.call_counter
        self.a(return_adress)
        self.call_counter += 1
        self.c('D', 'A')
        self.a('SP')
        self.c('M', 'D')
        self.a('SP')
        self.c('M', 'M+1')

        # now saving the segments addresses
        for segment in Coder.SEGMENTS:
            self.a(segment)
            self.c('D', 'M')
            self.a('SP')
            self.c('M', 'D')
            self.a('SP')
            self.c('M', 'M+1')

        # now to reseting the local segment to the top of the stack:

        self.a('SP')
        self.c('D', 'M')
        self.a('LCL')
        self.c('M', 'D')

        # now defining the arguments segment:

        self.a('SP')
        self.c('D', 'M')
        self.a(str(args))
        self.c('D', 'D-A')
        self.a('ARG')
        self.c('M', 'D')

        # going for the function

        self.a(function_name)
        self.c('', '0', 'JMP')

        # and returning to the unique adress we started at:

        self.writeLabel(return_adress)

    def writeReturn(self):
        # this is what we do when encountering the return command

        # storing the lcl in a temp:

        self.a('LCL')
        self.c('D', 'M')
        self.a('R13')
        self.c('M', 'D')

        # return adress should be LCL - 5:

        self.a('5')

        # !!!!!!!! maybe bug prone notice!!! ###
        self.c('A', 'D-A')
        self.c('D', 'M')

        # now we have the return adress

        self.a('R14')
        self.c('M', 'D')

        # poping the arguments from the stack

        self.a('SP')
        self.c('A', 'M-1')
        self.c('D', 'M')
        self.a('ARG')
        self.c('A', 'M')
        self.c('M', 'D')
        self.a('SP')
        self.c('M', 'M-1')

        # arg+1 -> sp

        self.a('ARG')
        self.c('D', 'M+1')
        self.a('SP')
        self.c('M', 'D')

        # reseting segments:

        i = 1
        for segment in Coder.SEGMENTS:
            self.a('13')
            self.c('D', 'M')
            self.a(str(i))
            self.c('D', 'D-A')
            self.c('A', 'D')
            self.c('D', 'M')
            self.a(segment)
            self.c('M', 'D')
            i += 1

        # now going back to the return adress:

        self.a('14')
        self.c('A', 'M')
        self.c('', '0', 'JMP')

    def writeGoto(self, label):
        self.a(label)
        self.c('', '0', 'JMP')

    def writeIf(self, label):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M')
        self.a(label)
        self.c('', 'D', 'JNE')

    def close(self):
        self.output_file.close()

    def write_add(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M')
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', 'M+D')

    def write_sub(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M')
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', 'M-D')

    def write_neg(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', '-M')

    def write_eq(self):
        # making the value

        self.a('SP')
        self.c("AM", "M-1")
        self.c("D", "M")
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M-D')

        self.writeGoto("TRUE" + str(self.true_counter))
        self.c('', 'D', 'JEQ')

        # all the false part goes in here, no need to label

        self.a('SP')
        self.c('M', '0')

        self.writeGoto("END" + str(self.end_counter))
        self.c('', '0', 'JMP')

        # all the true part goes in here, WE NEED TO LABEL
        self.writeLabel("TRUE" + str(self.true_counter))
        self.true_counter += 1

        self.a('SP')
        self.c('M', '-1')

        # end label
        self.writeLabel("END" + str(self.end_counter))
        self.end_counter += 1

    def write_gt(self):
        self.a('SP')
        self.c("AM", "M-1")
        self.c("D", "M")
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M-D')

        self.writeGoto("TRUE" + str(self.true_counter))
        self.c('', 'D', 'JGT')

        # all the false part goes in here, no need to label

        self.a('SP')
        self.c('M', '0')

        self.writeGoto("END" + str(self.end_counter))
        self.c('', '0', 'JMP')

        # all the true part goes in here, WE NEED TO LABEL
        self.writeLabel("TRUE" + str(self.true_counter))
        self.true_counter += 1

        self.a('SP')
        self.c('M', '-1')

        # end label
        self.writeLabel("END" + str(self.end_counter))
        self.end_counter += 1

    def write_lt(self):
        self.a('SP')
        self.c("AM", "M-1")
        self.c("D", "M")
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M-D')

        self.writeGoto("TRUE" + str(self.true_counter))
        self.c('', 'D', 'JLT')

        # all the false part goes in here, no need to label

        self.a('SP')
        self.c('M', '0')

        self.writeGoto("END" + str(self.end_counter))
        self.c('', '0', 'JMP')

        # all the true part goes in here, WE NEED TO LABEL
        self.writeLabel("TRUE" + str(self.true_counter))
        self.true_counter += 1

        self.a('SP')
        self.c('M', '-1')

        # end label
        self.writeLabel("END" + str(self.end_counter))
        self.end_counter += 1

    def write_and(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M')
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', 'M&D')

    def write_or(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('D', 'M')
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', 'M|D')

    def write_not(self):
        self.a('SP')
        self.c('AM', 'M-1')
        self.c('M', '!M')
