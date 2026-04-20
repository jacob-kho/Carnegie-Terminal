def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5


def getVolatility(data):
    mean = sum(data) / len(data)
    squared = [(v - mean) ** 2 for v in data]
    sdv = (sum(squared) / len(squared)) ** 0.5
    return sdv
