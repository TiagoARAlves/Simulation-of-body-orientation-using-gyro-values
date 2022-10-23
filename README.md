# Simulation-of-body-orientation-using-gyro-values
Graphical simulation of the orientation of a body using its angular velocity data over time. The angular velocity values can be obtained, for example, by an arduino reading an IMU. The important thing is to get the data as shown in the "data.txt" file, so that it can be handled by the program.

**The software presents a correct way of calculating orientation and the wrong way that is widespread in the community.** It shows the final differences between the two methods.

![](https://github.com/TiagoARAlves/Simulation-of-body-orientation-using-gyro-values/blob/main/animation.gif)

# Program dependencies:
- Matplotlib
- Numpy

# Important informations:
- The  considered coordinate system is the right-handed-z-up
- The name of the file into which the gyro data should be placed is "data.txt"
- "data.txt" lines structure:

    *microseconds passed since esp32 initialization;rad/s on x-axis; rad/s on y-axis; rad/s on z-axis*
- "output.txt" lines structure (considers the unit vectors i, j, k to be of the body frame with respect to the inertial frame):

    *ix;iy;iz;jx;jy;jz;kx;ky;kz*
- The data in "output.txt" is presented in time order, but the time instants are not specified. For this reason, the simulation is done in temporal order but is not to scale
- It is assumed that the body frame at the initial moment matches the inertial frame
