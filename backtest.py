from cmu_graphics import *


def drawBacktest(app):

    # Canvas
    drawRect(10, 50, app.width - 20, app.height - 60,
             fill=app.BG, border=app.BORDER, borderWidth=1)
    drawLabel('Backtest Results', app.width // 2, app.titleY + 10,
              size=10, bold=True, fill=app.TEXT_PRI)

    # Nav Buttons
    menuColor = app.HOVER_BIN if app.menuHoverB else app.PANEL
    drawRect(10, 5, 50, 20, fill=menuColor, border=app.BORDER, borderWidth=1)
    drawLabel('Main Menu', 35, 15, size=5, fill=app.TEXT_SEC)

    portfolioColor = app.HOVER_BIN if app.portfolioHoverB else app.PANEL
    drawRect(app.width - 60, 5, 50, 20, fill=portfolioColor, border=app.BORDER, borderWidth=1)
    drawLabel('Portfolio', app.width - 35, 15, size=5, fill=app.TEXT_SEC)

    if len(app.backtestResults) < 2:
        return

    # Chart Bounds
    chartLeft = 48
    chartRight = app.width - 32
    chartTop = 70
    chartBottom = app.height - 30
    maxVal = max(app.backtestResults)
    minVal = min(app.backtestResults)

    # Axes
    drawLine(chartLeft, chartTop, chartLeft, chartBottom, fill=app.BORDER)
    drawLine(chartLeft, chartBottom, chartRight, chartBottom, fill=app.BORDER)

    # Animated Equity Curve
    points = min(app.backtestStep, len(app.backtestResults))
    lineColor = app.GREEN_ACC if app.backtestResults[-1] >= 100 else app.CRIMSON
    for i in range(1, points):
        x1 = chartLeft + (i - 1) * (chartRight - chartLeft) / (len(app.backtestResults) - 1)
        x2 = chartLeft + i * (chartRight - chartLeft) / (len(app.backtestResults) - 1)
        y1 = chartBottom - (app.backtestResults[i - 1] - minVal) / (maxVal - minVal) * (chartBottom - chartTop)
        y2 = chartBottom - (app.backtestResults[i] - minVal) / (maxVal - minVal) * (chartBottom - chartTop)
        drawLine(x1, y1, x2, y2, fill=lineColor, lineWidth=1.5)

    # Y-axis Guidelines
    numLabels = 5
    for i in range(numLabels + 1):
        val = minVal + (maxVal - minVal) * i / numLabels
        y = chartBottom - (val - minVal) / (maxVal - minVal) * (chartBottom - chartTop)
        drawLabel(f"{val:.0f}", chartLeft - 15, y, size=5, fill=app.TEXT_SEC)
        drawLine(chartLeft, y, chartRight, y, fill=app.BORDER, opacity=30)

    # Hover Crosshair
    if app.hoverWeek is not None:
        hx = chartLeft + app.hoverWeek * (chartRight - chartLeft) / (len(app.backtestResults) - 1)
        drawLine(hx, chartTop, hx, chartBottom, fill=app.GOLD, opacity=50, dashes=True)
        drawLabel(f"Week {app.hoverWeek}: ${app.hoverValue:.2f}", hx, chartTop - 10,
                  size=6, fill=app.GOLD, bold=True)

    # Metrics Box
    totalReturn = (app.backtestResults[-1] - 100) / 100
    retCol = app.GREEN_ACC if totalReturn >= 0 else app.CRIMSON
    mw, mh = 100, 80
    drawRect(app.metricsX - mw / 2, app.metricsY, mw, mh,
             fill=app.PANEL, border=app.CRIMSON, borderWidth=1)
    drawLabel('Metrics', app.metricsX, app.metricsY + 13, size=7, bold=True, fill=app.TEXT_PRI)
    drawLabel(f"Return: {totalReturn:.1%}", app.metricsX, app.metricsY + 28, size=6, fill=retCol)
    drawLabel(f"Volatility: {app.volatility:.2%}", app.metricsX, app.metricsY + 40, size=6, fill=app.TEXT_PRI)
    drawLabel(f"Sharpe: {app.sharpeRatio:.2f}", app.metricsX, app.metricsY + 52, size=6, fill=app.TEXT_PRI)
    drawLabel(f"Max DD: {app.maxDrawdown:.1%}", app.metricsX, app.metricsY + 64, size=6, fill=app.CRIMSON)

    # Help Button
    helpColor = app.HOVER_BIN if app.onHelp else app.PANEL
    drawCircle(app.helpCX, app.helpCY, app.helpR, fill=helpColor, border=app.BORDER, borderWidth=1)
    drawLabel('?', app.helpCX, app.helpCY, size=8, bold=True, fill=app.TEXT_SEC)
