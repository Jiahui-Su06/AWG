import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

# 测试代码
lambda_um = np.linspace(0.5, 0.9, 401)
n = Air(lambda_um)

plt.plot(lambda_um, n)
plt.xlabel("Wavelength (µm)")
plt.ylabel("Refractive index")
plt.grid(True)
plt.show()

print(Air(0.6))