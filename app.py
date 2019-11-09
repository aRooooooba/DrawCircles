import wx
import math

class MyFrame(wx.Frame):
    """
    The main frame.
    """

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self, id=wx.WindowIDRef(-1))
        
        # 20 * 20 buttons
        self.buttonPool = []
        for i in range(20):
            for j in range(20):
                button = wx.Button(
                        panel,
                        # reord the index of the button in its ID
                        id = wx.WindowIDRef(100 * i + j),
                        label = '',
                        pos = ((i + 1) * 20, (j + 1) * 20),
                        size = (10, 10)
                        )
                # original colour is grey
                button.SetBackgroundColour(wx.Colour(180, 180, 180))
                button.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
                button.Bind(wx.EVT_MOTION, self.onMotion)
                button.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
                self.buttonPool.append(button)

        # use status bar to show the position of the mouse
        self.CreateStatusBar()
        panel.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        panel.Bind(wx.EVT_MOTION, self.onMotion)
        panel.Bind(wx.EVT_LEFT_UP, self.onLeftUp)

    def onLeftDown(self, event):
        """
        Invoke when pressing on left.
        Record the center of the circle.
        """
        
        # initialize the colour of the buttons
        [btn.SetBackgroundColour(wx.Colour(180, 180, 180)) for btn in self.buttonPool]
        mouseEvent = wx.MouseEvent(event)
        self.center = self.getPosition(
                mouseEvent.GetLogicalPosition(wx.ClientDC(self)).Get(),
                mouseEvent.GetEventObject().GetId()
                )
        self.SetStatusText(str(self.center))

    def onMotion(self, event):
        """
        Invoke when moving the mouse.
        Draw a circle on the screen.
        """

        mouseEvent = wx.MouseEvent(event)
        # process only when left is being pressed
        if mouseEvent.Dragging():
            # get the current position
            position = self.getPosition(
                    mouseEvent.GetLogicalPosition(wx.ClientDC(self)).Get(),
                    mouseEvent.GetEventObject().GetId()
                    )
            # calculate the radius
            self.radius = math.sqrt((position[0] - self.center[0]) ** 2 + (position[1] - self.center[1]) ** 2)
            dc = wx.ClientDC(self)
            # remove the previous circles
            dc.Clear()
            # force to refresh
            self.Refresh()
            self.Update()
            dc.SetPen(wx.Pen(wx.Colour(0, 0, 255)))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), style=wx.BRUSHSTYLE_TRANSPARENT))
            dc.DrawCircle(*self.center, self.radius)

    def onLeftUp(self, event):
        """
        Invoke when left is released.
        Generate the final graph.
        """

        # keep track of the maximum dist and the minimum dist
        maxDist, minDist = 0, 600
        for button in self.buttonPool:
            # get the position of the center of each point
            centerOfPoint = self.getPosition([5, 5], button.GetId())
            # make the button blue if it is close to the border of the circle
            dist = math.sqrt((centerOfPoint[0] - self.center[0]) ** 2 + (centerOfPoint[1] - self.center[1]) ** 2)
            if self.radius - 9 < dist < self.radius + 9:
                button.SetBackgroundColour(wx.Colour(0, 0, 255))
                # the thickness of each point is 5, so +/-5 is needed to avoid the red circles from going through the points
                if dist + 5 > maxDist:
                    maxDist = dist + 5
                elif dist - 5 < minDist:
                    minDist = dist - 5
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), style=wx.BRUSHSTYLE_TRANSPARENT))
        dc.DrawCircle(*self.center, maxDist)
        dc.DrawCircle(*self.center, minDist)


    def getPosition(self, position, objectId):
        """
        Get real position.
        param position: relative position
        param objectId: the ID of the object that triggers the event
        return: [int] * 2, real position
        """
        
        if objectId < 0:
            # click on panel, record the position directly
            return list(position)
        else:
            # click on button, position is relative within the button, need to add offset
            return [position[0] + (objectId // 100 + 1) * 20, position[1] + (objectId % 100 + 1) * 20]



app = wx.App()
frame = MyFrame(None, title='Draw Circles', size=(440,480))
frame.Show()
app.MainLoop()
