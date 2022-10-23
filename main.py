from QuadTree import *
from PIL import Image
from matplotlib.pyplot import gray
from numpy import array

def main():
    gray()
    img = array(Image.open('image.jpg').convert('L'), dtype='float64')
    #img = mpimg.imread('image.jpg')
    #img.shape

    quadtree = QuadTree().insert(img)
    cluster = quadtree.get_cluster(2)
    print(cluster)Compilacion

    plt.imshow(quadtree.get_image(2))
    plt.show()
    plt.imshow(quadtree.get_border(2))
    plt.show()
    plt.imshow(quadtree.get_image(3))
    plt.show()
    plt.imshow(quadtree.get_border(3))
    plt.show()
    plt.imshow(quadtree.get_image(4))
    plt.show()
    plt.imshow(quadtree.get_border(4))
    plt.show()
    
    plt.imshow(quadtree.get_image(5))
    plt.show()
    plt.imshow(quadtree.get_border(5))
    plt.show()
    plt.imshow(quadtree.get_image(6))
    plt.show()
    plt.imshow(quadtree.get_border(6))
    plt.show()
main()
