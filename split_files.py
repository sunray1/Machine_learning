import os, sys, csv

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        print(line)
        subgenus = line[3]
        if subgenus == "unidentified":
        	os.system("mv bees_hires/%s %s" % (line[0]+".jpg", "unknown"))
        
        
# Subgenus	
# ?	6
# Alpigenobombus	55
# Alpinobombus	1556
# Bombias	259
# Bombus	4803
# Cullumanobombus	2067
# Kallobombus	43
# Megabombus	475
# Melanobombus	705
# Mendacibombus	32
# Orientalibombus	37
# Psithyrus	1054
# Pyrobombus	17457
# Sibiricobombus	8
# Subterraneobombus	454
# Thoracobombus	4344
        
    
