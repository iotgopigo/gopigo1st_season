
def array (rect):
    del rect[:]
    rect.append([1,2])
    rect.append([3,4])
    rect.append([5,6])
    rect.append([7,8])
    return True


if __name__ == "__main__":
    rect = []
    for num in range(2): 
        array(rect)
        print rect
