from cmu_graphics import *
from data.stocks import loadStockData
from screens.welcome import drawWelcome
from screens.screener import drawScreener, getSortKey
from screens.portfolio import drawPortfolio
from screens.backtest import drawBacktest
from logic.backtest import runBacktest
from logic.optimizer import optimizeWeights
from utils import distance


def onAppStart(app):

    # Background
    app.url = 'cmu://1166281/46516607/abstract-polygonal-shape-black-background-free-vector.jpg'

    # Design Tokens
    app.BG = rgb(13, 17, 23)
    app.PANEL = rgb(22, 27, 34)
    app.BORDER = rgb(48, 54, 61)
    app.CRIMSON = rgb(196, 30, 58)
    app.CRIMSON_DIM = rgb(139, 0, 0)
    app.RED_DIM = rgb(70, 15, 25)
    app.GOLD = rgb(255, 195, 0)
    app.TEXT_PRI = rgb(230, 237, 243)
    app.TEXT_SEC = rgb(139, 148, 158)
    app.TEXT_HEAD = rgb(255, 255, 255)
    app.GREEN_ACC = rgb(35, 197, 94)
    app.GREEN_DIM = rgb(20, 60, 35)
    app.ROW_EVEN = rgb(22, 27, 34)
    app.ROW_A = rgb(13, 17, 23)
    app.ROWB = rgb(22, 27, 34)
    app.BLUE_PILL = rgb(31, 56, 100)
    app.HOVER_BIN = rgb(48, 54, 61)

    # Navigation
    app.currentScreen = 'welcome'

    # Welcome Hover
    app.screenerHoverW = False
    app.portfolioHoverW = False

    # Screener
    app.stocks = loadStockData()
    app.selectedStocks = []
    app.headers = ['Ticker', 'Name', 'Sector', 'P/E', 'Growth', 'Price', 'Return']
    app.sortBy = None
    app.sortReverse = False
    app.filterSector = 'All'
    app.sectors = ['All', 'Tech', 'Semiconductor', 'Finance', 'Healthcare', 'Energy', 'Auto']
    app.titleY = app.width / 25
    app.filterY = 37.5
    app.tableTop = 60

    # Screener Hover
    app.menuHoverS = False
    app.portfolioHoverS = False

    # Portfolio Builder
    app.weights = {}
    app.tableTopPort = 60
    app.buttonWidth = 45
    app.buttonHeight = 14

    # Portfolio Builder Hover
    app.menuHoverP = False
    app.screenerHoverP = False

    # Backtest
    app.backtestResults = []
    app.backtestStep = 0
    app.backtestRunning = False

    # Backtest Hover
    app.menuHoverB = False
    app.portfolioHoverB = False

    # Chart Hover
    app.hoverWeek = None
    app.hoverValue = 0

    # Metrics
    app.totalReturn = 0
    app.volatility = 0
    app.sharpeRatio = 0
    app.maxDrawdown = 0
    app.metricsX = app.width - 80
    app.metricsY = 60
    app.metricsDragging = False

    # Help
    app.showHelpScreener = False
    app.showHelpPortfolioBuilder = False
    app.showHelpBacktest = False
    app.onHelp = False
    app.helpCX = app.width - 12.5
    app.helpCY = app.height - 12.5
    app.helpR = 7.5


def redrawAll(app):

    # Background
    drawImage(app.url, 0, 0, width=app.width, height=app.height,
              opacity=100, rotateAngle=0, align='left-top', visible=True)

    # Route to active screen
    if app.currentScreen == 'welcome':
        drawWelcome(app)
    elif app.currentScreen == 'screener':
        drawScreener(app)
    elif app.currentScreen == 'portfolio':
        drawPortfolio(app)
    elif app.currentScreen == 'backtest':
        drawBacktest(app)

    # Help overlays
    if app.showHelpScreener:
        drawRect(0, 0, app.width, app.height, fill=app.BG, opacity=90)
        drawLabel('                 Terminal Screener Manual', app.width // 2, 30,
                  size=12, bold=True, fill=app.TEXT_PRI)
        drawLabel('Carnegie', app.width // 2 - 76, 30, size=12, bold=True, fill=app.CRIMSON)
        drawLabel('Sort stocks by alphabetical or numerical order by clicking headers',
                  app.width // 2, 60, size=7, fill=app.TEXT_SEC)
        drawLabel('Press sector buttons to filter by sector', app.width // 2, 80, size=7, fill=app.TEXT_SEC)
        drawLabel('Press portfolio to go to portfolio builder', app.width // 2, 100, size=7, fill=app.TEXT_SEC)
        drawLabel('Click anywhere to close', app.width // 2, 130, size=6, fill=app.TEXT_SEC)

    elif app.showHelpPortfolioBuilder:
        drawRect(0, 0, app.width, app.height, fill=app.BG, opacity=90)
        drawLabel('                 Terminal Portfolio Builder Manual', app.width // 2, 30,
                  size=12, bold=True, fill=app.TEXT_PRI)
        drawLabel('Carnegie', app.width // 2 - 96, 30, size=12, bold=True, fill=app.CRIMSON)
        drawLabel('Click + to add stock and adjust weights with -/+', app.width // 2, 60, size=7, fill=app.TEXT_SEC)
        drawLabel('Once at 100% weight, click backtest to view animated equity curve and performance metrics',
                  app.width // 2, 80, size=7, fill=app.TEXT_SEC)
        drawLabel('Press optimize to find the best weight allocation to maximize Sharpe ratio for up to 5 stocks',
                  app.width // 2, 100, size=7, fill=app.TEXT_SEC)
        drawLabel('Press screener to return to screener', app.width // 2, 120, size=7, fill=app.TEXT_SEC)
        drawLabel('Click anywhere to close', app.width // 2, 150, size=6, fill=app.TEXT_SEC)

    elif app.showHelpBacktest:
        drawRect(0, 0, app.width, app.height, fill=app.BG, opacity=90)
        drawLabel('                 Terminal Backtest Manual', app.width // 2, 30,
                  size=12, bold=True, fill=app.TEXT_PRI)
        drawLabel('Carnegie', app.width // 2 - 75, 30, size=12, bold=True, fill=app.CRIMSON)
        drawLabel('Drag the metrics box to reposition it', app.width // 2, 60, size=7, fill=app.TEXT_SEC)
        drawLabel('Hover over the equity curve to view historical portfolio value',
                  app.width // 2, 80, size=7, fill=app.TEXT_SEC)
        drawLabel('Click portfolio to return to portfolio builder', app.width // 2, 100, size=7, fill=app.TEXT_SEC)
        drawLabel('Click anywhere to close', app.width // 2, 130, size=6, fill=app.TEXT_SEC)


def onStep(app):
    if app.backtestRunning:
        app.backtestStep += 2
        if app.backtestStep >= len(app.backtestResults):
            app.backtestRunning = False


def onMousePress(app, mouseX, mouseY):

    # Welcome
    if app.currentScreen == 'welcome':
        if (app.width // 2 - 120 <= mouseX <= app.width // 2 - 10
                and app.titleY + 195 <= mouseY <= app.titleY + 235):
            app.currentScreen = 'screener'
        if (app.width // 2 + 10 <= mouseX <= app.width // 2 + 120
                and app.titleY + 195 <= mouseY <= app.titleY + 235):
            app.currentScreen = 'portfolio'

    # Screener
    if app.currentScreen == 'screener':
        if app.showHelpScreener:
            app.showHelpScreener = False
            return
        if distance(mouseX, mouseY, app.helpCX, app.helpCY) <= app.helpR:
            app.showHelpScreener = True
            return
        headers = app.headers
        deltaX = app.width / (len(headers) + 1)
        deltaY = app.height / (len(app.stocks) + 3)
        if app.filterY - app.buttonHeight / 2 <= mouseY <= app.filterY + app.buttonHeight / 2:
            for sector in range(len(app.sectors)):
                x = deltaX * (sector + 1)
                if x - app.buttonWidth / 2 <= mouseX <= x + app.buttonWidth / 2:
                    app.filterSector = app.sectors[sector]
        if deltaY * 1.5 <= mouseY <= deltaY * 2.5:
            for col in range(len(headers)):
                if deltaX * (col + 0.5) <= mouseX <= deltaX * (col + 1.5):
                    if app.sortBy == headers[col]:
                        app.sortReverse = not app.sortReverse
                    else:
                        app.sortBy = headers[col]
                        app.sortReverse = False
        if 10 <= mouseX <= 60 and 5 <= mouseY <= 25:
            app.currentScreen = 'welcome'
        if app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25:
            app.currentScreen = 'portfolio'

    # Portfolio
    elif app.currentScreen == 'portfolio':
        if app.showHelpPortfolioBuilder:
            app.showHelpPortfolioBuilder = False
            return
        if distance(mouseX, mouseY, app.helpCX, app.helpCY) <= app.helpR:
            app.showHelpPortfolioBuilder = True
            return
        if 10 <= mouseX <= 60 and 5 <= mouseY <= 25:
            app.currentScreen = 'welcome'

        headers = ['Ticker', 'Name', 'Price', 'Select', 'Weight', 'Adjust']
        deltaX = app.width / (len(headers) + 1)
        deltaY = (app.height - app.tableTopPort) / (len(app.stocks) + 3)
        for index, ticker in enumerate(app.stocks):
            row = app.tableTopPort + deltaY * (index + 2) - 15
            if (deltaX * 4 - 8 <= mouseX <= deltaX * 4 + 8
                    and row - 8 <= mouseY <= row + 8):
                if ticker in app.selectedStocks:
                    app.selectedStocks.remove(ticker)
                    if ticker in app.weights:
                        del app.weights[ticker]
                else:
                    app.selectedStocks.append(ticker)
                    app.weights[ticker] = 0
                return
            if ticker in app.selectedStocks:
                total = sum(app.weights.values())
                if (deltaX * 6 - 18 <= mouseX <= deltaX * 6 - 6
                        and row - 6 <= mouseY <= row + 6):
                    if app.weights[ticker] > 0:
                        app.weights[ticker] -= 10
                    return
                if (deltaX * 6 + 2 <= mouseX <= deltaX * 6 + 14
                        and row - 6 <= mouseY <= row + 6):
                    if app.weights[ticker] < 100 and total != 100:
                        app.weights[ticker] += 10
                    return

        total = sum(app.weights.values())
        bottomY = app.tableTopPort + deltaY * (len(app.stocks) + 2.5)
        if total == 100:
            if (deltaX * 6 - 25 <= mouseX <= deltaX * 6 + 25
                    and bottomY - 35 <= mouseY <= bottomY - 15):
                app.currentScreen = 'backtest'
                runBacktest(app)
        if 6 > len(app.selectedStocks) > 0:
            if (deltaX * 6 - 25 <= mouseX <= deltaX * 6 + 25
                    and bottomY - 13 <= mouseY <= bottomY + 7):
                optimizeWeights(app)
        if app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25:
            app.currentScreen = 'screener'

    # Backtest
    elif app.currentScreen == 'backtest':
        if app.showHelpBacktest:
            app.showHelpBacktest = False
            return
        if distance(mouseX, mouseY, app.helpCX, app.helpCY) <= app.helpR:
            app.showHelpBacktest = True
            return
        if 10 <= mouseX <= 60 and 5 <= mouseY <= 25:
            app.currentScreen = 'welcome'
        if app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25:
            app.currentScreen = 'portfolio'
        mw, mh = 100, 80
        if (app.metricsX - mw / 2 <= mouseX <= app.metricsX + mw / 2
                and app.metricsY <= mouseY <= app.metricsY + mh):
            app.metricsDragging = True


def onMouseDrag(app, mouseX, mouseY):
    mh = 80
    if app.metricsDragging:
        app.metricsX = mouseX
        app.metricsY = mouseY - mh / 2


def onMouseMove(app, mouseX, mouseY):

    # Help button
    app.onHelp = distance(mouseX, mouseY, app.helpCX, app.helpCY) <= app.helpR

    # Backtest chart hover
    if app.currentScreen == 'backtest' and len(app.backtestResults) > 1:
        chartLeft = 48
        chartRight = app.width - 32
        if chartLeft <= mouseX <= chartRight:
            ratio = (mouseX - chartLeft) / (chartRight - chartLeft)
            weekIndex = int(ratio * (len(app.backtestResults) - 1))
            weekIndex = max(0, min(weekIndex, len(app.backtestResults) - 1))
            app.hoverWeek = weekIndex
            app.hoverValue = app.backtestResults[weekIndex]
        else:
            app.hoverWeek = None

    # Welcome hover
    if app.currentScreen == 'welcome':
        app.screenerHoverW = (app.width // 2 - 120 <= mouseX <= app.width // 2 - 10
                               and app.titleY + 195 <= mouseY <= app.titleY + 235)
        app.portfolioHoverW = (app.width // 2 + 10 <= mouseX <= app.width // 2 + 120
                                and app.titleY + 195 <= mouseY <= app.titleY + 235)

    # Screener hover
    elif app.currentScreen == 'screener':
        app.menuHoverS = (10 <= mouseX <= 60 and 5 <= mouseY <= 25)
        app.portfolioHoverS = (app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25)

    # Portfolio hover
    elif app.currentScreen == 'portfolio':
        app.menuHoverP = (10 <= mouseX <= 60 and 5 <= mouseY <= 25)
        app.screenerHoverP = (app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25)

    # Backtest hover
    elif app.currentScreen == 'backtest':
        app.menuHoverB = (10 <= mouseX <= 60 and 5 <= mouseY <= 25)
        app.portfolioHoverB = (app.width - 60 <= mouseX <= app.width - 10 and 5 <= mouseY <= 25)


def onMouseRelease(app, mouseX, mouseY):
    app.metricsDragging = False


def main():
    runApp()


main()
