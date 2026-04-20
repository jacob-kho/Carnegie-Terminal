from cmu_graphics import *


def drawWelcome(app):

    # Panel
    drawRect(app.width // 2 - 172.5, app.height // 2 - 82.5, 350, 150,
             fill=app.PANEL, border=app.CRIMSON, borderWidth=1)
    drawLabel('Welcome to                 Terminal', app.width // 2, app.titleY + 130,
              size=20, bold=True, fill=app.TEXT_PRI)
    drawLabel('Carnegie', app.width // 2 + 16, app.titleY + 130,
              size=20, bold=True, fill=app.CRIMSON)
    drawLabel('Press a button to start!', app.width // 2, app.titleY + 155,
              size=10, bold=True, fill=app.TEXT_SEC)

    # Screener Button
    screenerColor = app.HOVER_BIN if app.screenerHoverW else app.PANEL
    drawRect(app.width // 2 - 120, app.titleY + 195, 110, 40,
             fill=screenerColor, border=app.CRIMSON, borderWidth=1)
    drawLabel('Screener', app.width // 2 - 65, app.titleY + 215,
              size=10, bold=True, fill=app.TEXT_PRI)

    # Portfolio Builder Button
    portfolioColor = app.HOVER_BIN if app.portfolioHoverW else app.PANEL
    drawRect(app.width // 2 + 10, app.titleY + 195, 110, 40,
             fill=portfolioColor, border=app.BORDER, borderWidth=1)
    drawLabel('Portfolio Builder', app.width // 2 + 65, app.titleY + 215,
              size=10, bold=True, fill=app.TEXT_SEC)
