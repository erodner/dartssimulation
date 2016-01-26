import matplotlib.pylab as plt

# copied from: http://stackoverflow.com/questions/14754931/matplotlib-values-under-cursor
def show_value_under_cursor(img):
    def format_coord(img, x, y):
        numrows, numcols = img.shape
        col = int(x+0.5)
        row = int(y+0.5)
        if col>=0 and col<numcols and row>=0 and row<numrows:
            z = img[row,col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f'%(x, y)

    plt.gca().format_coord = lambda x,y: format_coord(img, x, y)

