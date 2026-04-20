from cmu_graphics import *


def drawPortfolio(app):

    # Title
    drawLabel('Portfolio Builder', app.width // 2, app.titleY + 20,
              size=10, bold=True, fill=app.TEXT_PRI)

    # Nav Buttons
    menuColor = app.HOVER_BIN if app.menuHoverP else app.PANEL
    drawRect(10, 5, 50, 20, fill=menuColor, border=app.BORDER, borderWidth=1)
    drawLabel('Main Menu', 35, 15, size=5, fill=app.TEXT_SEC)

    screenerColor = app.HOVER_BIN if app.screenerHoverP else app.PANEL
    drawRect(app.width - 60, 5, 50, 20, fill=screenerColor, border=app.BORDER, borderWidth=1)
    drawLabel('Screener', app.width - 35, 15, size=5, fill=app.TEXT_SEC)

    # Table Setup
    headers = ['Ticker', 'Name', 'Price', 'Select', 'Weight', 'Adjust']
    deltaX = app.width / (len(headers) + 1)
    deltaY = (app.height - app.tableTopPort) / (len(app.stocks) + 3)

    # Header Row
    drawRect(deltaX * 0.5, app.tableTopPort, app.width - deltaX, deltaY,
             fill=app.PANEL, border=app.BORDER, borderWidth=1)
    for col in range(len(headers)):
        drawLabel(headers[col], deltaX * (col + 1), app.tableTopPort + deltaY / 2,
                  size=6, bold=True, fill=app.TEXT_SEC)

    # Stock Rows
    for index, ticker in enumerate(app.stocks):
        stock = app.stocks[ticker]
        row = app.tableTopPort + deltaY * (index + 2) - 15
        color = app.ROW_EVEN if index % 2 == 0 else app.ROW_A
        drawRect(deltaX * 0.5, row - deltaY / 2, app.width - deltaX, deltaY,
                 fill=color, border=app.BORDER, borderWidth=0.5)

        drawLabel(ticker, deltaX * 1, row, size=6, fill=app.GOLD, bold=True)
        drawLabel(stock.name, deltaX * 2, row, size=6, fill=app.TEXT_PRI)
        drawLabel(f"${stock.prices[-1]:.2f}", deltaX * 3, row, size=6, fill=app.TEXT_PRI)

        # Select Toggle
        if ticker in app.selectedStocks:
            btnColor, btnBorder, btnLabel, btnTextCol = app.RED_DIM, app.CRIMSON, '-', app.CRIMSON
        else:
            btnColor, btnBorder, btnLabel, btnTextCol = app.GREEN_DIM, app.GREEN_ACC, '+', app.GREEN_ACC
        drawRect(deltaX * 4 - 8, row - 8, 16, 16, fill=btnColor, border=btnBorder, borderWidth=1)
        drawLabel(btnLabel, deltaX * 4, row, size=8, fill=btnTextCol, bold=True)

        # Weight Controls
        if ticker in app.selectedStocks:
            weight = app.weights.get(ticker, 0)
            drawLabel(f"{weight}%", deltaX * 5, row, size=6, fill=app.GOLD, bold=True)
            drawRect(deltaX * 6 - 18, row - 6, 12, 12, fill=app.RED_DIM, border=app.CRIMSON, borderWidth=1)
            drawLabel('-', deltaX * 6 - 12, row, size=7, fill=app.CRIMSON, bold=True)
            drawRect(deltaX * 6 + 2, row - 6, 12, 12, fill=app.GREEN_DIM, border=app.GREEN_ACC, borderWidth=1)
            drawLabel('+', deltaX * 6 + 8, row, size=7, fill=app.GREEN_ACC, bold=True)

    # Footer
    total = sum(app.weights.values())
    totalColor = app.GREEN_ACC if total == 100 else app.CRIMSON
    bottomY = app.tableTopPort + deltaY * (len(app.stocks) + 2.5)

    drawRect(deltaX * 4 + 25, bottomY - 35, 114, 42, fill=app.PANEL, border=app.BORDER, borderWidth=1)
    drawLabel(f"Total: {total}%", deltaX * 5, bottomY - 15, size=8, fill=totalColor, bold=True)

    # Backtest Button
    if total == 100:
        drawRect(deltaX * 6 - 25, bottomY - 35, 50, 20, fill=app.CRIMSON, border=app.CRIMSON, borderWidth=1)
    else:
        drawRect(deltaX * 6 - 25, bottomY - 35, 50, 20, fill=app.RED_DIM, border=app.CRIMSON, borderWidth=1)
    drawLabel('Backtest', deltaX * 6, bottomY - 25, size=6, fill=app.TEXT_HEAD, bold=True)

    # Optimize Button
    if 6 > len(app.selectedStocks) > 0:
        drawRect(deltaX * 6 - 25, bottomY - 13, 50, 20, fill=app.GREEN_ACC, borderWidth=1)
        drawLabel('Optimize', deltaX * 6, bottomY - 3, size=6, fill=app.GREEN_DIM, bold=True)
    else:
        drawRect(deltaX * 6 - 25, bottomY - 13, 50, 20, fill=app.GREEN_DIM, border=app.GREEN_ACC, borderWidth=1)
        drawLabel('Optimize', deltaX * 6, bottomY - 3, size=6, fill=app.GREEN_ACC, bold=True)

    # Help Button
    helpColor = app.HOVER_BIN if app.onHelp else app.PANEL
    drawCircle(app.helpCX, app.helpCY, app.helpR, fill=helpColor, border=app.BORDER, borderWidth=1)
    drawLabel('?', app.helpCX, app.helpCY, size=8, bold=True, fill=app.TEXT_SEC)
