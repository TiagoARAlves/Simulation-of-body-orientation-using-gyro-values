import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

class Vetores:
    def __init__(self, data):
        self.data = data
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        self.ax.axes.set_xlim3d(-1.5, 1.5)
        self.ax.axes.set_ylim3d(-1.5, 1.5)
        self.ax.axes.set_zlim3d(-1.5, 1.5)
        self.x = self.ax.quiver(0, 0, 0, 1, 0, 0)
        self.x.set_color('r')
        self.y = self.ax.quiver(0, 0, 0, 0, 1, 0)
        self.y.set_color('g')
        self.z = self.ax.quiver(0, 0, 0, 0, 0, 1)
        self.z.set_color('b')

    def animate(self, i):
        self.x.remove()
        self.y.remove()
        self.z.remove()
        self.x = self.ax.quiver(0, 0, 0, self.data[i][0], self.data[i][1], self.data[i][2])
        self.x.set_color('r')
        self.y = self.ax.quiver(0, 0, 0, self.data[i][3], self.data[i][4], self.data[i][5])
        self.y.set_color('g')
        self.z = self.ax.quiver(0, 0, 0, self.data[i][6], self.data[i][7], self.data[i][8])
        self.z.set_color('b')
    
    def startAni(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=self.data.size, interval=10, repeat=False)
        plt.show()

def simula():
    try:
        with open('output.txt', 'r') as f:
            data = np.array(f.readlines())
            f.close()
    except IOError:
        print('\n\nNão existe o ficheiro \"output.txt\"!')
        input('Pressione qualquer tecla para fechar o programa...')
        quit()

    data = np.char.strip(data, '\n')
    data = np.char.split(data, ';')
    for c in range(data.size):
        data[c] = np.array(data[c]).astype(np.single)
    data = data[::10]

    v = Vetores(data)
    v.startAni()

if __name__=='__main__':
    simula()
    input('Pressione qualquer tecla para fechar o programa...')