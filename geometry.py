# Very very very small module to define code that is reused too often


def rotate1(block, forward=True):
    "Rotate one block: make first element last (forward), and vice-versa"
    if forward:
	return block[1:] + block[0:1]
    else:
	return block[-1:] + block[0:-1]
