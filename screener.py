from cmu_graphics import *


def getSortKey(app, ticker):
    stock = app.stocks[ticker]
    if app.sortBy == 'P/E':
        return stock.pe
    elif app.sortBy == 'Growth':
        return stock.revenueGrowth
    elif app.sortBy == 'Price':
        return stock.prices[-1]
    elif app.sortBy == 'Return':
        return stock.getReturn(0, len(stock.prices) - 1)
    elif app.sortBy == 'Name':
        return stock.name
    elif app.sortBy == 'Sector':
        return stock.sector
    elif app.sortBy == 'Ticker':
        return ticker
    else:
        return ticker


def drawScreener(app):

    # Title
    drawLabel('Screener', app.width // 2, app.titleY, size=10, bold=True, fill=app.TEXT_PRI)

    headers = ['Ticker', 'Name', 'Sector', 'P/E', 'Growth', 'Price', 'Return']
    deltaX = app.width / (len(headers) + 1)
    deltaY = app.height / (len(app.stocks) + 3)

    # Sector Filter Buttons
    for sector in range(len(app.sectors)):
        x = deltaX * (sector + 1)
        color = app.BLUE_PILL if app.sectors[sector] == app.filterSector else app.PANEL
        borderCol = app.CRIMSON if app.sectors[sector] == app.filterSector else app.BORDER
        drawRect(x - app.buttonWidth / 2, deltaY - app.buttonHeight / 2 + 7,
                 app.buttonWidth, app.buttonHeight, fill=color, border=borderCol, borderWidth=1)
        textCol = app.TEXT_HEAD if app.sectors[sector] == app.filterSector else app.TEXT_SEC
        drawLabel(app.sectors[sector], x, app.filterY, size=5, fill=textCol)

    # Header Row
    drawRect(deltaX * 0.5, deltaY * 1.5, app.width - deltaX, deltaY,
             fill=app.PANEL, border=app.BORDER, borderWidth=1)

    # Sorting
    if app.sortBy:
        pairs = []
        for ticker in app.stocks:
            pairs.append((getSortKey(app, ticker), ticker))
        pairs.sort(reverse=app.sortReverse)
        tickers = [pair[1] for pair in pairs]
    else:
        tickers = list(app.stocks)

    # Sector Filtering
    if app.filterSector != 'All':
        filtered = []
        for ticker in tickers:
            if app.stocks[ticker].sector == app.filterSector:
                filtered.append(ticker)
        tickers = filtered

    # Table
    for col in range(len(headers)):
        drawLabel(headers[col], deltaX * (col + 1), deltaY * 2, size=6, bold=True, fill=app.TEXT_SEC)
    for index, ticker in enumerate(tickers):
        stock = app.stocks[ticker]
        row = app.tableTop + deltaY * (index + 1)
        ret = stock.getReturn(0, len(stock.prices) - 1)
        retColor = app.GREEN_ACC if ret >= 0 else app.CRIMSON
        color = app.ROW_EVEN if index % 2 == 0 else app.ROW_A
        drawRect(deltaX * 0.5, row - deltaY / 2, app.width - deltaX, deltaY,
                 fill=color, border=app.BORDER)
        drawLabel(ticker, deltaX * 1, row, size=6, fill=app.GOLD, bold=True)
        drawLabel(stock.name, deltaX * 2, row, size=6, fill=app.TEXT_PRI)
        drawLabel(stock.sector, deltaX * 3, row, size=6, fill=app.TEXT_SEC)
        drawLabel(stock.pe, deltaX * 4, row, size=6, fill=app.TEXT_PRI)
        drawLabel(f"{stock.revenueGrowth:.1%}", deltaX * 5, row, size=6, fill=app.TEXT_PRI)
        drawLabel(f"{stock.prices[-1]:.2f}", deltaX * 6, row, size=6, fill=app.TEXT_PRI)
        drawLabel(f"{ret:.1%}", deltaX * 7, row, size=6, fill=retColor, bold=True)

    # Nav Buttons
    portfolioColor = app.HOVER_BIN if app.portfolioHoverS else app.PANEL
    drawRect(app.width - 60, 5, 50, 20, fill=portfolioColor, border=app.BORDER, borderWidth=1)
    drawLabel('Portfolio', app.width - 35, 15, size=5, fill=app.TEXT_SEC)

    menuColor = app.HOVER_BIN if app.menuHoverS else app.PANEL
    drawRect(10, 5, 50, 20, fill=menuColor, border=app.BORDER, borderWidth=1)
    drawLabel('Main Menu', 35, 15, size=5, fill=app.TEXT_SEC)

    # Help Button
    helpColor = app.HOVER_BIN if app.onHelp else app.PANEL
    drawCircle(app.helpCX, app.helpCY, app.helpR, fill=helpColor, border=app.BORDER, borderWidth=1)
    drawLabel('?', app.helpCX, app.helpCY, size=8, bold=True, fill=app.TEXT_SEC)
