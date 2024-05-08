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

    return peaks

def getPeaks(ranks: list[int], points: list[int]):
    """
    Prints the location of the r-th most prominent peaks for each r in ranks as well as its prominence height given a set of points
    """
    
    peaks = getPeakList(points)

    for peak in peaks:
        print(peak)



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
