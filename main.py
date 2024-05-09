import sys

class Peak:
    def __init__(self, index, point, left = 0, right = 0) -> None:
        self.index = index
        self.point = point
        self.right = right
        self.left = left
        self.prominence = None
    
    def __str__(self) -> str:
        return f"[ INDEX: {self.index} | POINT: {self.point} | LEFT: {self.left} | RIGHT: {self.right} | PROMINENCE: {self.prominence} ]"
    
def getPeakList(points: list[int]):
    peaks: list[Peak] = []
    newLowest = True
    currLowest = 0
    # In one pass, we can set all left and right points for each peak
    for i, point in enumerate(points):
        print(f"Analyzing {i} / 199997")

        # First point may be a peak
        if i == 0:
            if point > points[1]: 
                peaks.append(Peak(i, point, left=0))
            else:
                newLowest = False
                currLowest = point

        # Last point may be a peak
        elif i == len(points)-1:
            if point > points[-2]: 
                if len(peaks) != 0: 
                    peaks[-1].right = currLowest
                peaks.append(Peak(i, point, left=currLowest))
            else:
                peaks[-1].right = 0

        # Middle points
        else:

            # If we find a peak...
            if point > points[i-1] and point > points[i+1]:
                if len(peaks) != 0: 
                    peaks[-1].right = currLowest
                peaks.append(Peak(i, point, left=currLowest))
                newLowest = True
            else:
                if newLowest:
                    newLowest = False
                    currLowest = point
                else: 
                    if point < currLowest:
                        currLowest = point
    
    # We can now calculate the prominence for each peak
    # Efficiency - can also do this if u keep track of the highest peak rankings (in the peak object), like the highest peak is 1, second highest is 2... 
    # this could make it calculatable in the one pass? for now we do this
    _ = len(peaks)
    for i, peak in enumerate(peaks):
        # For each peak, look to the left and right to find the prominently relevant peaks
        # Look left for the highest peak to the left, also keeping track of the lowest current point between
        print(f"Prominence calculation {i} / {_}")
        colLeft = peak.left
        peakExists = False
        if i == 0: colLeft = 0
        for left in range(i-1,-1,-1):
            if peaks[left].point > peak.point:
                peakExists = True
                break
            else:
                if peaks[left].left < colLeft: colLeft = peaks[left].left
                if left == 0 and peakExists == False:
                    colLeft = 0
        
        colRight = peak.right
        peakExists = False
        if i == len(peaks): colRight = 0
        for right in range(i+1, len(peaks)):
            if peaks[right].point > peak.point:
                peakExists = True 
                break
            else:
                if peaks[right].right < colRight: colRight = peaks[right].right
                if right == len(peaks) - 1 and peakExists == False:
                    colRight = 0

        # print(f"For {peak.point}, left relevant is {colLeft}, right relevant is {colRight}")
        peak.prominence = peak.point - max(colLeft, colRight)

    peaks.sort(key=lambda peak: peak.prominence, reverse=True)
    return peaks

def isPeak(i: int, points: list[int]) -> bool:
    """
    Given an index and a point list, returns whether or not the point at that index is a peak
    """
    if i == 0:
        return True if points[0] > points[1] else False
    elif i == len(points) - 1:
        return True if points[-1] > points[-2] else False
    elif points[i] > points[i-1] and points[i] > points[i+1]: return True
    else: return False
                
def getPeaks(ranks: list[int], points: list[int]):
    """
    Prints the index & prominence of the r-th most prominent peaks for each r in ranks as well as its prominence height given a set of points
    """
    # LEFT PASS
    indexToCols: dict[int: list[int]] = {}
    stack: list[list] = [] # (index, point, left lowest)
    lowestGlobal = 0
    for i, point in enumerate(points):
        print(f"Checking point {i} / 199997")
        # print(f"\nChecking point {i}: {point}...")
        if isPeak(i, points):                                       # Check if the point is a peak
            # print(f"\tPoint is a peak! Finding relevant left...")
            lowest = 0
            largerPeak = None
            while len(stack) != 0 and stack[-1][1] < point:
                popped = stack.pop()
                if lowest == 0 or popped[2] < lowest:
                    lowest = popped[2]
            if len(stack) != 0:
                largerPeak = stack[-1]
                lowest = min(points[stack[-1][0]:i])
                # print(f"\tThe stack item with the larger peak is {stack[-1]} and the lowest point is {lowest}")
            else:
                lowest = 0
            # print(f"\tAppending {[i, point, lowest]} to the stack")
            stack.append([i, point, lowest])
            indexToCols[i] = [lowest]
        else:                                                       # If the point is not a peak
            if len(stack) != 0 and (point < stack[-1][2] or stack[-1][2] == 0):
                # print(f"\tPoint is not a peak... but will replace {stack[-1]} to", end=" ")
                stack[-1][2] = point
                # print(f"{stack[-1]}")
            if lowestGlobal == 0 or lowestGlobal > point:
                lowestGlobal = point
        # print(f"Stack is now {stack}")
        # print(f"Lowest global is {lowestGlobal}")
    
    # for x, y in indexToCols.items():
    #     print(x, y)
    
    # RIGHT PASS
    stack: list[list] = [] # (index, point, left lowest)
    lowestGlobal = 0
    points = list(reversed(points))
    for i, point in enumerate(points):
        print(f"Checking point {i} / 199997")
        # print(f"\nChecking point {i}: {point}...")
        if isPeak(i, points):                                       # Check if the point is a peak
            # print(f"\tPoint is a peak! Finding relevant left...")
            lowest = 0
            largerPeak = None
            while len(stack) != 0 and stack[-1][1] < point:
                popped = stack.pop()
                if lowest == 0 or popped[2] < lowest:
                    lowest = popped[2]
            if len(stack) != 0:
                largerPeak = stack[-1]
                lowest = min(points[stack[-1][0]:i]) # potential source of the inefficiency here - can this be calculated on the fly?
                # print(f"\tThe stack item with the larger peak is {stack[-1]} and the lowest point is {lowest}")
            else:
                lowest = 0
            # print(f"\tAppending {[i, point, lowest]} to the stack")
            stack.append([i, point, lowest])
            indexToCols[(len(points)-1)-i].append(lowest)
            lowestGlobal = 0
        else:                                                       # If the point is not a peak
            if len(stack) != 0 and (point < stack[-1][2] or stack[-1][2] == 0):
                # print(f"\tPoint is not a peak... but will replace {stack[-1]} to", end=" ")
                stack[-1][2] = point
                # print(f"{stack[-1]}")
            if lowestGlobal == 0 or lowestGlobal > point:
                lowestGlobal = point
        # print(f"Stack is now {stack}")
        # print(f"Lowest global is {lowestGlobal}")
    
    # for x, y in indexToCols.items():
    #     print(x, y)

    points = list(reversed(points))
    peaks = []
    for index, cols in indexToCols.items():
        peaks.append((index, points[index] - max(cols[0], cols[1])))
    peaks.sort(key=lambda x: x[1], reverse=True)
    
    for rank in ranks:
        try:
            index, prominence = peaks[rank-1]
        except:
            index, prominence = (0, 0)
        print(index, prominence)

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