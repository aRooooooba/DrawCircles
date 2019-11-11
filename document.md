# Draw Circles

## Demands

Start with a single window containing a grid of $20\times20$ points.

All points start out grey.

The user click to place the center of a circle, drag to set its radius. At the same time, the circle should be drawn.

When releasing the mouse button, highlight the points (make them blue) that correspond to the edge of the circle.

Two additional circles should be created corresponding to the largest and smallest radius of the highlighted points.



## Environment

Ubuntu 18.04.3 LTS, Vim, Python 3.6.8, wxPython 4



## Structure

**class MyFrame(wx.Frame)**

Methods

---

- \_\_init\_\_(*self, \*args, \*\*kw*)

  \_\_init\_\_(*self*)

  \_\_init\_\_(*self, parent, id=ID_ANY, title='', pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr*)

  Constructor, creating the window, including the $20\times20$ points, panel and status bar. It is also responsible for binding events.

- onLeftDown(*self, event*)

  Invoke when the left mouse button changes to down. All the buttons return to their initiate status to start a new round. At this time, the position of the circle center will be recorded, which is exactly the position of the pressing of the mouse happens.

- onMotion(*self, event*)

  Invoke when moving the mouse, no matter whether the left mouse button is being pressed. So firstly, check if it is being pressed, if not, return directly.

  Keep track of the mouse position. Calculate the radius with the center and the current position. Refresh the window to get rid of the previous circles and draw a new circle with center and radius.

- onLeftUp(*self, event*)

  Invoke when the left mouse button changes to up. Traverse all points. Turn their colour into blue if they are close to the border of the circle.

  Find the outermost and the innermost points within the blue points, calculate their distance to the center, and draw another two red circles.

- getPosition(*self, position, objectId*)

  Get the relative position in the window.

  **Parameters**

  - position: the relative position in the points
  - objectId: the id of the target point

  When constructing, the objectId contains the index of each point. If an event happens within a point, only the relative position within the point will be returned. So an offset is needed to acquire the relative position in the window.

  

Properties

---

- buttonPool: stores all the $20\times20$ points
- center: the position of the center of the circle
- radius: the radius of the circle



## Result

![Screenshot from 2019-11-09 16-49-49](/home/xingjian/Pictures/Screenshot from 2019-11-09 16-49-49.png)

![Screenshot from 2019-11-09 16-50-11](/home/xingjian/Pictures/Screenshot from 2019-11-09 16-50-11.png)

![Screenshot from 2019-11-09 16-50-33](/home/xingjian/Pictures/Screenshot from 2019-11-09 16-50-33.png)

![Screenshot from 2019-11-09 16-50-48](/home/xingjian/Pictures/Screenshot from 2019-11-09 16-50-48.png)

![Screenshot from 2019-11-09 16-51-05](/home/xingjian/Pictures/Screenshot from 2019-11-09 16-51-05.png)



## To be improved

It's not very smooth when dragging a circle.