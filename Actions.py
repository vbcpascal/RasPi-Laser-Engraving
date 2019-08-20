import os

import numpy as np

# modes of actions
ACT_MOVE = 0
ACT_WORK = 1
ACT_OPEN_LASER = 2
ACT_CLOSE_LASER = 3


# a list of actions. each element is shown as [ACT, x, y] or [ACT]
class Actions:
    def __init__(self):
        self.work_list = []
        self.group_length = 0
        self.length = 0

    def push(self, action, point=None):
        if action == ACT_MOVE or action == ACT_WORK:
            self.work_list.append([action, point[0], point[1]])
        else:
            self.work_list.append([action])

    def clear(self):
        self.work_list.clear()
        self.group_length = 0

    def top_pop(self):
        act = self.work_list[0]
        self.work_list = self.work_list[1:]
        self.length -= 1
        if act[0] == ACT_CLOSE_LASER:
            self.group_length -= 1
        return act

    def len(self):
        return self.length

    def group_len(self):
        return self.group_length

    def empty(self):
        return self.work_list == []

    def save(self, filename):
        return np.save(filename, self.work_list)

    def load(self, filename):
        self.work_list = np.load(filename, allow_pickle=True)

    def add_contours(self, reader):
        import ImageReader as ir
        assert(reader.get_mode() == ir.MODE_CONTOURS)
        contours = reader.get_contours()
        self.group_length = len(contours)

        for contour in contours:
            start_point = contour[0][0]
            self.push(ACT_MOVE, start_point)
            self.push(ACT_OPEN_LASER)

            for point in contour[1:]:
                self.push(ACT_WORK, point[0])

            self.push(ACT_CLOSE_LASER)
        self.push(ACT_MOVE, [0, 0])

        self.length = len(self.work_list)


if __name__ == "__main__":
    import ImageReader as ir
    imr = ir.ImageReader(os.path.join('pics', 'logo.png'))
    imr.set_mode(ir.MODE_CONTOURS)
    acts = Actions()
    acts.add_contours(imr)
    acts.save(os.path.join('cache', 'logo.npy'))
    print(acts.top_pop())
    print(acts.group_len())
    print(len(acts.work_list))
