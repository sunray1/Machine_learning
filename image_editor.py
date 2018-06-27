#!/usr/bin/env python

import sys, os
import PythonMagick as Magick
from argparse import ArgumentParser
import random

argp = ArgumentParser(description='Edits jpg images for deep learning')
argp.add_argument('-i', '--indir', help='location of directory containing files', required=True)
argp.add_argument('-o', '--outdir', help='output directory name (will create if doesn\'t exist', required=True)
argp.add_argument('-f', '--flipflop', help='flips/flops images', action='store_true')
argp.add_argument('-r', '--rotate', help='rotates images', type=int)
argp.add_argument('-c', '--complementary', help='changes images into complementary colors', action='store_true')
argp.add_argument('-g', '--grayscale', help='changes images into grayscale', action='store_true')
argp.add_argument('-z', '--zoom', help='zooms to a particular pixel by inputted factor', type=float)
argp.add_argument('-col', '--color', help='color filter', action='store_true')
argp.add_argument('-p', '--crop', help='crop to 220x298', action='store_true')
argp.add_argument('-n', '--noise', help='add Guassian noise', action='store_true')

args = argp.parse_args()

dirin = args.indir
jpgfiles = [f for f in os.listdir(dirin) if f.endswith('.jpg')]

if os.path.exists(args.outdir) == False:
    os.mkdir(args.outdir)
outdir = args.outdir + "/"
for jpg in jpgfiles:
    img = Magick.Image(dirin.rstrip('/')+"/"+jpg)
    pre_suff = jpg.split(".")
    
    if args.flipflop == True:
        img.flip()
        img.write(outdir+pre_suff[0]+"_FLIPPED."+pre_suff[1])
        img.flop()
        img.write(outdir+pre_suff[0]+"_FLIPPED_FLOPPED."+pre_suff[1])
        img.flip()
        img.write(outdir+pre_suff[0]+"_FLOPPED."+pre_suff[1])
        img.flop()
    
    if args.rotate:
        img.rotate(args.rotate)
        img.crop(Magick.Geometry(220, 298, 0, 0))
        img.sample(str(220) + "x" + str(298) + "!")
        img.write(outdir+pre_suff[0]+"_ROTATED"+str(args.rotate)+"."+pre_suff[1])
        img = Magick.Image(dirin.rstrip('/')+"/"+jpg)
        
    if args.complementary == True:
        img.negate()
        img.write(outdir+pre_suff[0]+"_COMPLEMENT."+pre_suff[1])
        img.negate()

    if args.grayscale == True:
        img.colorSpace(Magick.ColorspaceType.GRAYColorspace)
        img.write(outdir+pre_suff[0]+"_GRAYSCALE."+pre_suff[1])
        img = Magick.Image(dirin.rstrip('/')+"/"+jpg)
        
    if args.zoom:
        #crop and zoom
        width = img.size().width()
        height = img.size().height()
        factor = args.zoom
        zoombyxw = int(round(width/factor))
        zoombyxh = int(round(height/factor))
        #140x200 is the center pixel in which we are zooming to
        leftcornerwpix = int(round(140 - (width/(factor*2))))
        leftcornerhpix = int(round(200 - (height/(factor*2))))
        img.crop(Magick.Geometry(zoombyxw, zoombyxh, leftcornerwpix, leftcornerhpix))
        img.sample(str(width) + "x" + str(height) + "!")
        img.write(outdir+pre_suff[0]+"_ZOOM"+str(int(args.zoom))+"."+pre_suff[1])
        
    if args.color:
        color = random.choice(["red", "green", "blue"])
        img.colorize(10,10,10, color)
        img.write(outdir+pre_suff[0]+"_COLORIZE."+pre_suff[1])

    if args.crop == True:
        img.crop(Magick.Geometry(170, 248, 50, 50))
        img.sample(str(220) + "x" + str(298) + "!")
        img.write(outdir+pre_suff[0]+"_CROP."+pre_suff[1])
        img = Magick.Image(dirin.rstrip('/')+"/"+jpg)
        
    if args.noise == True:
        img_in = dirin.rstrip('/')+"/"+jpg
        img_out = outdir+pre_suff[0]+"_NOISE."+pre_suff[1]
        os.system("magick %s -attenuate .5 +noise Impulse %s" % (img_in, img_out))
        