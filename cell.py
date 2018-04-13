class Pixel:
    def __init__(self, genome, pos_x, pos_y):
        self.genome = genome
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_genome(self):
        return self.genome

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
