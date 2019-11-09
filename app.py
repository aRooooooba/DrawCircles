import wx
import time
import math

class MyFrame(wx.Frame):
    """
    The main frame.
    """

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.panel = wx.Panel(self, id=wx.WindowIDRef(-1))
        
        # 20 * 20 buttons
        self.buttonPool = []
        for i in range(20):
            for j in range(20):
                button = wx.Button(
                        self.panel,
                        # reord the index of the button in its ID
                        id = wx.WindowIDRef(100 * i + j),
                        label = '',
                        pos = ((i + 1) * 20, (j + 1) * 20),
                        size = (10, 10)
                        )
                # original colour is grey
                button.SetBackgroundColour(wx.Colour(180,180,180))
                button.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
                button.Bind(wx.EVT_MOTION, self.onMotion)
                self.buttonPool.append(button)

        # use status bar to show the position of the mouse
        self.CreateStatusBar()
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.panel.Bind(wx.EVT_MOTION, self.onMotion)

    def onLeftDown(self, event):
        """
        Invoke when pressing on left.
        Record the center of the circle.
        """
        
        mouseEvent = wx.MouseEvent(event)
        position = mouseEvent.GetLogicalPosition(wx.ClientDC(self)).Get()
        objectId = mouseEvent.GetEventObject().GetId()
        self.center = self.getPosition(position, objectId)
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
            dc.Clear()
            self.Refresh()
            self.Update()
            dc.SetPen(wx.Pen(wx.Colour(0, 0, 255)))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), style=wx.BRUSHSTYLE_TRANSPARENT))
            dc.DrawCircle(*self.center, self.radius)

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
frame = MyFrame(None, title='buttontest', size=(440,480))
frame.Show()
app.MainLoop()
