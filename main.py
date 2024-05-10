class Peak:
    def __init__(self, index, point) -> None:
        self.index = index
        self.point = point
    def __str__(self) -> str:
        return f"Peak at index {self.index} of height {self.point}"
    
class Col:
    def __init__(self, value) -> None:
        self.value = value
    def __str__(self) -> str:
        return f"Col of height {self.value}"
    
def isPeak(i: int, points: list[int]) -> bool:
    """
    Given an index and a point list, returns whether or not the point at that index is a peak
    """
    if i == 0:
        return True if points[0] > points[1] else False
    elif i == len(points) - 1:
        return True if points[-1] > points[-2] else False
    elif points[i] > points[i-1] and points[i] > points[i+1]:
        return True
    else: return False
                
def getPeaks(ranks: list[int], points: list[int]):
    """
    Prints the index & prominence of the r-th most prominent peaks for each r in ranks as well as its prominence height given a set of points
    """
    stack = [None]
    indexToCol: dict[int:list] = {}
    for i, point in enumerate(points):

        if len(stack) % 2 == 1:
            last: Col = stack[-1]

            if last == None:
                stack.append(Peak(i, point))
                continue
            
            if last.value > point:
                stack[-1] = Col(point)
            else:
                while len(stack) != 0:
                    col_l = stack.pop()
                    prevPeak = stack.pop()
                    if prevPeak.point > point:
                        if isPeak(i, points):
                            indexToCol[i] = [col_l.value]
                        stack.append(prevPeak)
                        stack.append(col_l)
                        stack.append(Peak(i, point))
                        break
                    else:
                        col_r = stack.pop()
                        if len(stack) == 0:
                            if isPeak(i, points):
                                indexToCol[i] = [0]
                            stack.append(None)
                            stack.append(Peak(i, point))
                            break
                        else:
                            stack.append(Col(min(col_l.value, col_r.value)))

        else:

            last: Peak = stack[-1]
            
            if point < last.point:
                stack.append(Col(point))
            else:
                stack.pop()
                if stack[-1] == None:
                    if isPeak(i, points):
                        indexToCol[i] = [0]
                    stack.append(Peak(i, point))
                    continue
                
                while len(stack) != 0:
                    col_l = stack.pop()
                    prevPeak = stack.pop()
                    if prevPeak.point > point:
                        if isPeak(i, points):
                            indexToCol[i] = [col_l.value]
                        stack.append(prevPeak)
                        stack.append(col_l)
                        stack.append(Peak(i, point))
                        break
                    else:
                        col_r = stack.pop()
                        if len(stack) == 0:
                            if isPeak(i, points):
                                indexToCol[i] = [0]
                            stack.append(None)
                            stack.append(Peak(i, point))
                            break
                        else:
                            stack.append(Col(min(col_l.value, col_r.value)))

    stack = [None]
    points = list(reversed(points))
    for i, point in enumerate(points):

        if len(stack) % 2 == 1:
            last: Col = stack[-1]

            if last == None:
                stack.append(Peak(i, point))
                continue
            
            if last.value > point:
                stack[-1] = Col(point)
            else:
                while len(stack) != 0:
                    col_l = stack.pop()
                    prevPeak = stack.pop()
                    if prevPeak.point > point:
                        if isPeak(i, points):
                            indexToCol[(len(points)-1)-i].append(col_l.value)
                        stack.append(prevPeak)
                        stack.append(col_l)
                        stack.append(Peak(i, point))
                        break
                    else:
                        col_r = stack.pop()
                        if len(stack) == 0:
                            if isPeak(i, points):
                                indexToCol[(len(points)-1)-i].append(0)
                            stack.append(None)
                            stack.append(Peak(i, point))
                            break
                        else:
                            stack.append(Col(min(col_l.value, col_r.value)))

        else:
            last: Peak = stack[-1]
            
            if point < last.point:
                stack.append(Col(point))
            else:
                stack.pop()
                if stack[-1] == None:
                    if isPeak(i, points):
                        indexToCol[(len(points)-1)-i].append(0)
                    stack.append(Peak(i, point))
                    continue
                
                while len(stack) != 0:
                    col_l = stack.pop()
                    prevPeak = stack.pop()
                    if prevPeak.point > point:
                        if isPeak(i, points):
                            indexToCol[(len(points)-1)-i].append(col_l.value)
                        stack.append(prevPeak)
                        stack.append(col_l)
                        stack.append(Peak(i, point))
                        break
                    else:
                        col_r = stack.pop()
                        if len(stack) == 0:
                            if isPeak(i, points):
                                indexToCol[(len(points)-1)-i].append(0)
                            stack.append(None)
                            stack.append(Peak(i, point))
                            break
                        else:
                            stack.append(Col(min(col_l.value, col_r.value)))
    
    points = list(reversed(points))
    prominences = [(x, points[x] - max(y[0], y[1])) for x, y in indexToCol.items()]
    prominences.sort(key=lambda p: p[1], reverse=True)
    for rank in ranks:
        try:
            print(prominences[rank-1])
        except:
            print((0, 0))

if __name__ == "__main__":

    file = open("input.txt")

    ranks = []
    points = []
    numPoints = int(file.readline())
    numRanks = int(file.readline())

    while numPoints != 0:
        points.append(int(file.readline().strip("\n")))
        numPoints -= 1
    
    while numRanks != 0:
        ranks.append(int(file.readline().strip("\n")))
        numRanks -= 1
    
    getPeaks(ranks, points)