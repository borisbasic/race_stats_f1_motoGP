import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
plt.figure()
image = plt.imread(r'moto_gp_images_racers/noun-motogp-4891316.jpg')
image = image.resize((100, 100))
plt.imshow(image) 
plt.show()