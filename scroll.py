from sys import argv
from PIL import Image
import argparse


    # Box is (left, upper, right, lower) in describing pixel length
    #     upper
    #   x-------x 
    # l |    |  | r
    # e |  x--x | i
    # f |--|  |-| g
    # t |  x--x | h
    #   |    |  | t
    #   x-------x
    #     lower

def hroll(image: Image.Image, delta: int) -> Image.Image:
    """Roll an image sideways."""
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))

    return image


# TODO implement this!!!!
def vroll(image: Image.Image, delta: int) -> Image.Image:
    """Roll an image vertically"""
    xsize, ysize = image.size

    delta = delta % ysize
    if delta == 0: return image

    part1 = image.crop((0, 0, xsize, delta))
    part2 = image.crop((0, delta, xsize, ysize))

    image.paste(part1, (0, ysize-delta, xsize, ysize)) 
    image.paste(part2, (0, 0, xsize, ysize-delta))

    return image



def froll(image: Image.Image, delta: int) -> Image.Image:
    vroll(image, delta)
    hroll(image, delta)
    return image 


parser = argparse.ArgumentParser(description="Scroll image and output a copy of it")
#add args
parser.add_argument("-d", "--dir", choices=["h", "v", "f"], 
                    default="f", 
                    help="Direction of scroll. Options are horizontal (h), vertical (v) or default both (f)")

parser.add_argument("-o", "--out", metavar="path",help="Location to store scrolled file")

# parser.add_argument("-w", "--horizontal", action="store_const", const=0, dest="mode")
# parser.add_argument("-v", "--vertical", action="store_const", const=1, dest="mode")
# parser.add_argument("-f", "--full", action="store_const", const=2, dest="mode")

parser.add_argument("image", help="Path to image")
parser.add_argument("delta", nargs="?",type=int, 
                    choices=range(0,101), metavar="delta",
                    default="50", help="Percentage of screen to shift")

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    im = Image.open(args.image)

    delta = args.delta * (1 / 100)
    dh = int(im.size[0] * delta)
    dv = int(im.size[1] * delta)

    if args.dir == 'h':
        hroll(im, dh)
    elif args.dir == 'v':
        vroll(im, dv)
    else: #for 'f'
        hroll(im, dh)
        vroll(im, dv)

    # now to store the name
    name = args.out if args.out is not None else args.image.split(".")[0] + "-scroll.bmp"
    im.save(name, "BMP")
