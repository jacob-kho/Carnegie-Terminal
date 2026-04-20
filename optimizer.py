from logic.backtest import runBacktest


def optimizeWeights(app):
    bestResult = [-1000, {}]
    currentWeights = {}
    optimizeHelper(app, 0, 100, currentWeights, bestResult)
    app.weights = bestResult[1]
    runBacktest(app)


def optimizeHelper(app, stockIndex, remainingWeight, currentWeights, bestResult):
    if stockIndex == len(app.selectedStocks):
        if remainingWeight == 0:
            app.weights = currentWeights
            runBacktest(app)
            if app.sharpeRatio > bestResult[0]:
                bestResult[0] = app.sharpeRatio
                bestResult[1] = dict(currentWeights)
        return
    ticker = app.selectedStocks[stockIndex]
    for weight in range(0, remainingWeight + 1, 10):
        currentWeights[ticker] = weight
        optimizeHelper(app, stockIndex + 1, remainingWeight - weight,
                       currentWeights, bestResult)
    del currentWeights[ticker]
