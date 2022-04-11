from tkinter import *
import math as m
import random as r

window = Tk()
window.geometry("800x800")
window.title("3D rendering engine")
window.resizable(width=False, height=False)
canvas = Canvas(window, width=800, height=800, background="white")
canvas.place(x=0, y=0)

camDist = 600;
camera = [m.pi/4, 0.5, camDist]
sDist = 200
allObjects = []
currentXYZCamCoords = [0, 0, 0]


def drawAllObjects():
   reOrderObjects()
   print("starting rendering...")
   for i in range(len(allObjects)):
      print("rendering ", i, " of ", len(allObjects), " objects...   -", int(i/len(allObjects)*100), "%", end='\r')
      allObjects[i].draw()
   print("all objects rendered.")
   print("rendering finished.")
      


def reOrderObjects():
   global allObjects
   global currentXYZCamCoords
   currentXYZCamCoords = xyzCamCoords(camera)
   for i in range(len(allObjects)):
      allObjects[i].getDistanceToCam(currentXYZCamCoords)
   newOrder = [allObjects[0]]
   allObjects.pop(0)
   for i in range(len(allObjects)):
      j = 0
      while j < len(newOrder) and newOrder[j].squareDistanceToCam < allObjects[i].squareDistanceToCam:
         j += 1
      newOrder.insert(j, allObjects[i])
   allObjects = newOrder




def render(point):
   alpha = -camera[0];
   beta = camera[1];
   x = -point[0]
   y = -point[1]
   z = -point[2]
   trans1x = m.cos(alpha)*(x + (z * m.tan(alpha)));
   trans1y = y;
   trans1z = (z / m.cos(alpha)) - (trans1x * m.tan(alpha));
   xNew = trans1x;
   yNew = m.cos(beta)*(trans1y + (trans1z * m.tan(beta)));
   zNew = (trans1z / m.cos(beta)) - (yNew * m.tan(beta));
   relativePointPos = [xNew, yNew, zNew];
   xProj = xNew / (camera[2] - zNew) * (camera[2] + sDist);
   yProj = yNew / (camera[2] - zNew) * (camera[2] + sDist);
   newPoint = (xProj+400, yProj+400);
   return newPoint;

def squareDistance(point1, point2):
   dist = m.pow(point2[0]-point1[0], 2) + m.pow(point2[1]-point1[1], 2) + m.pow(point2[2]-point1[2], 2)
   return dist
   
   

def xyzCamCoords(camera):
   y = camera[2]*m.sin(camera[1])
   grndDiag = m.sqrt(camera[2]*camera[2] - y*y)
   x = grndDiag * m.sin(camera[0])
   z = grndDiag * m.cos(camera[0])
   newCamPos = [x, y, z]
   return newCamPos

class Plane:
   def __init__(self, point1, point2, height, color, outline):
      self.point1 = [point1[0], height, point1[1]]
      self.point2 = [point1[0], height, point2[1]]
      self.point3 = [point2[0], height, point2[1]]
      self.point4 = [point2[0], height, point1[1]]
      self.centre = [(point1[0]+point2[0])/2, (point1[1]+point2[1])/2, height]
      self.color = color
      self.outline = outline
   
   def draw(self):
      self.pointsToDraw = [render(self.point1), render(self.point2), render(self.point3), render(self.point4)]
      canvas.create_polygon(self.pointsToDraw, fill=self.color, outline=self.outline, tag="iter")
      
   def getDistanceToCam(self, currentXYZCamCoords):
      print(currentXYZCamCoords)
      self.squareDistanceToCam = squareDistance(self.centre, currentXYZCamCoords)
      

      

class Sphere:
   def __init__(self, centre, radius):
      self.centre = centre
      self.radius = radius
   
   def draw(self):
      pass
   
   def getDistanceToCam(self, currentXYZCamCoords):
      self.squareDistanceToCam = squareDistance(self.centre, currentXYZCamCoords)
      
      
      
      
      
class Cube:
   def __init__(self, centre, size, color, outline):
      self.centre = centre
      self.size = size
      self.color = color
      self.outline = outline
      self.point1 = [self.centre[0] - self.size/2, self.centre[1] + self.size/2, self.centre[2] + self.size/2]
      self.point2 = [self.centre[0] + self.size/2, self.centre[1] + self.size/2, self.centre[2] + self.size/2]
      self.point3 = [self.centre[0] + self.size/2, self.centre[1] - self.size/2, self.centre[2] + self.size/2]
      self.point4 = [self.centre[0] - self.size/2, self.centre[1] - self.size/2, self.centre[2] + self.size/2]
      self.point5 = [self.centre[0] - self.size/2, self.centre[1] + self.size/2, self.centre[2] - self.size/2]
      self.point6 = [self.centre[0] + self.size/2, self.centre[1] + self.size/2, self.centre[2] - self.size/2]
      self.point7 = [self.centre[0] + self.size/2, self.centre[1] - self.size/2, self.centre[2] - self.size/2]
      self.point8 = [self.centre[0] - self.size/2, self.centre[1] - self.size/2, self.centre[2] - self.size/2]
      self.pointsToDraw = []

   def draw(self):
      camcoords = xyzCamCoords(camera)
      if squareDistance(camcoords, [self.centre[0],self.centre[1]+self.size/2,self.centre[2]]) >= squareDistance(camcoords, [self.centre[0],self.centre[1]-self.size/2,self.centre[2]]):
         self.pointsToDraw = [render(self.point3), render(self.point4), render(self.point8), render(self.point7)]
      else:
         self.pointsToDraw = [render(self.point1), render(self.point2), render(self.point6), render(self.point5)]
      canvas.create_polygon(self.pointsToDraw, fill=self.color, outline=self.outline, tag="iter")
      
      if squareDistance(camcoords, [self.centre[0]+self.size/2,self.centre[1],self.centre[2]]) >= squareDistance(camcoords, [self.centre[0]-self.size/2,self.centre[1],self.centre[2]]):
         self.pointsToDraw = [render(self.point2), render(self.point3), render(self.point7), render(self.point6)]
      else:
         self.pointsToDraw = [render(self.point1), render(self.point4), render(self.point8), render(self.point5)]
      canvas.create_polygon(self.pointsToDraw, fill=self.color, outline=self.outline, tag="iter")
      
      if squareDistance(camcoords, [self.centre[0],self.centre[1],self.centre[2]+self.size/2]) >= squareDistance(camcoords, [self.centre[0],self.centre[1],self.centre[2]-self.size/2]):
         self.pointsToDraw = [render(self.point1), render(self.point2), render(self.point3), render(self.point4)]
      else:
         self.pointsToDraw = [render(self.point5), render(self.point6), render(self.point7), render(self.point8)]
      canvas.create_polygon(self.pointsToDraw, fill=self.color, outline=self.outline, tag="iter")

   def getDistanceToCam(self, currentXYZCamCoords):
      self.squareDistanceToCam = squareDistance(self.centre, currentXYZCamCoords)
   

class Triangle:
   def __init__(self, point1, point2, point3, color, outline):
      self.color = color
      self.outline = outline
      self.point1 = point1
      self.point2 = point2
      self.point3 = point3
      self.centre = [(point1[0]+point2[0]+point3[0])/3, (point1[1]+point2[1]+point3[1])/3, (point1[2]+point2[2]+point3[2])/3]
   
   def draw(self):
      self.pointsToDraw = [render(self.point1), render(self.point2), render(self.point3)]
      canvas.create_polygon(self.pointsToDraw, fill=self.color, outline=self.outline, tag="iter")
   
   def getDistanceToCam(self, currentXYZCamCoords):
      self.squareDistanceToCam = squareDistance(self.centre, currentXYZCamCoords)
   
   
   

def keyPressed(event):
   global camera
   if event.keycode == 37:
      camera[0] -= 0.1
   if event.keycode == 38:
      camera[1] += 0.1
   if event.keycode == 39:
      camera[0] += 0.1
   if event.keycode == 40:
      camera[1] -= 0.1
   if event.keycode == 107:
      camera[2] -= 60
   if event.keycode == 109:
      camera[2] += 60
   if event.keycode == 13:
      createNewMap()
   else:
      canvas.delete("iter")
      drawAllObjects()





def createNewMap():

   global allObjects
   
   
   allObjects = []
   canvas.delete("all")
   iterations = 6
   pointNumber = int(m.pow(2, iterations))
   #allObjects.append(Plane([-200, -200], [200, 200], 0, "grey", "black"))

   """
   for i in range(pointNumber+1):
      Map.append([])
      for j in range(pointNumber+1):
         print("creating map matrix...               -", int((j+(pointNumber+1)*i)/((pointNumber+1)*(pointNumber+1))*100), "%", end='\r')
         Map[i].append([2])
         
   print("creating map matrix...               - 100 %", end='\r')
   print("")
   
   for i in range(pointNumber+1):
      for j in range(pointNumber+1):
         print("calculating height...                -", int((j+(pointNumber+1)*i)/((pointNumber+1)*(pointNumber+1))*100), "%", end='\r')
         Map[i][j] = [(Map[i][j-1][0]+Map[i-1][j][0])/2+r.randint(-8,8), "green"]
         
   print("calculating height...                - 100 %", end='\r')
   print("")
   
   """
   
   Map = [[[0]]]

   
   
   def iterate(Map):
   
      newMap = []

      for i in range(len(Map)*2):
         newMap.append([])
         for j in range(len(Map)*2):
            newMap[i].append([Map[m.floor(i/2)][m.floor(j/2)][0] + r.randint(-8, 8), "green"])

      return newMap
      
   for i in range(iterations):
      Map = iterate(Map)
   
   
   for i in range(pointNumber):
      for j in range(pointNumber):
         height = Map[i][j][0]
         green = hex(5*int(height)).replace("0x", "")
         if len(green) == 1:
            green = "0" + green
         if len(green) >= 3:
            green = "ff"
         color = "#" + green + "6a3d"
         Map[i][j][1] = color
         print("calculating colors...                -", int((j+(pointNumber+1)*i)/((pointNumber+1)*(pointNumber+1))*100), "%", end='\r')
         
   print("calculating colors...                - 100 %", end='\r')
   print("")
   
   for i in range(pointNumber):
      for j in range(pointNumber):
         if Map[i][j][0] < 0:
            height = Map[i][j][0]
            green = hex(abs(100+3*int(height))).replace("0x", "")
            if len(green) == 1:
               green = "0" + green
            if len(green) >= 3:
               green = "ff"
            color = "#3f" + green + "fe"
            Map[i][j] = [0, color]
         print("creating oceans...                   -", int((j+(pointNumber+1)*i)/((pointNumber+1)*(pointNumber+1))*100), "%", end='\r')
   
   print("creating oceans...                   - 100 %", end='\r')
   print("")

   for i in range(pointNumber-1):
      for j in range(pointNumber-1):
         k = 40/pointNumber
         allObjects.append(Triangle([-200+10*i*k, Map[i][j][0], -200+10*j*k], [-200+10*(i+1)*k, Map[i+1][j][0], -200+10*j*k], [-200+10*i*k, Map[i][j+1][0], -200+10*(j+1)*k], Map[i][j][1], Map[i][j][1]))
         allObjects.append(Triangle([-200+10*(i+1)*k, Map[i+1][j+1][0], -200+10*(j+1)*k], [-200+10*(i+1)*k, Map[i+1][j][0], -200+10*j*k], [-200+10*i*k, Map[i][j+1][0], -200+10*(j+1)*k], Map[i][j][1], Map[i][j][1]))
         print("creating parts...                    -", int((j+(pointNumber+1)*i)/((pointNumber+1)*(pointNumber+1))*100), "%", end='\r')
         
   print("creating parts...                    - 100 %", end='\r')
   print("")
         
   drawAllObjects()




createNewMap()


window.bind('<Key>', keyPressed)
window.mainloop()