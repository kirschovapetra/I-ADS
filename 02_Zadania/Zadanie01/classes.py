
class Word:
    def __init__(self, frequency, value):
        self.frequency = frequency
        self.value = value


class Tree:
    def __init__(self, value=""):
        self.value = value          # hodnota kluca
        self.left_subtree = None    # lavy podstrom
        self.right_subtree = None   # pravy podstrom

    def set_value(self, value):
        self.value = value

    def set_left_subtree(self, left_sub):
        self.left_subtree = left_sub

    def set_right_subtree(self, right_sub):
        self.right_subtree = right_sub

    def print_levels(self, save_to_file=False):
        """
        Vypis stromu po leveloch
        zdroj: https://www.geeksforgeeks.org/print-level-order-traversal-line-line/
        """
        output = ""
        queue = [self]

        # prechadzaju sa levely
        i = 1
        while queue:
            output += "\n--------------------------------\nLevel "+str(i) + ":\n"
            # prechadzaju sa uzly j v i-tom leveli
            j = len(queue)
            while j > 0:
                # zoberie sa uzol zo zaciatku queue
                temp = queue.pop(0)
                output += temp.value + "  "

                # enqueue vsetky uzly v lavom podstrome
                if temp.left_subtree:
                    queue.append(temp.left_subtree)

                # enqueue vsetky uzly v pravom podstrome
                if temp.right_subtree:
                    queue.append(temp.right_subtree)
                j -= 1
            i += 1

        if save_to_file:
            with open("tree.txt", "w") as f:
                f.write(output)

        print(output)
