import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )
    polygons=[]
    systems = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    edges=[]
    step_3d = 20

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        for c in commands:
            line=c[0]
            i=0
            j=0
            if line == 'sphere':
            #print 'SPHERE\t' + str(args)
                if not isinstance(c[1],float):
                    i=1
                add_sphere(polygons,float(c[1+i]), float(c[2+i]), float(c[3+i]),float(c[4+i]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line == 'torus':
                #print 'TORUS\t' + str(args)
                if not isinstance(c[1],float):
                    i=1
                add_torus(polygons,float(c[1+i]), float(c[2+i]), float(c[3+i]),float(c[4+i]), float(c[5+i]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line == 'box':
                #print 'BOX\t' + str(args)
                if not isinstance(c[1],float):
                    i=1
                add_box(polygons,float(c[1+i]), float(c[2+i]),float(c[3+i]), float(c[4+i]), float(c[5+i]), float(c[6+i]))
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []


            elif line == 'line':
                if not isinstance(c[1],float):
                    i=1
                if not isinstance(c[4+i],float):
                    j=1
                #print 'LINE\t' + str(args)

                add_edge( edges,float(c[1+i]), float(c[2+i]), float(c[3+i]),float(c[4+i+j]), float(c[5+i+j]), float(c[6+i+j]) )
                matrix_mult( systems[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []

            elif line == 'scale':
                #print 'SCALE\t' + str(args)
                t = make_scale(float(c[1]), float(c[2]), float(c[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]

            elif line == 'move':
                #print 'MOVE\t' + str(args)
                t = make_translate(float(c[1]), float(c[2]), float(c[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]

            elif line == 'rotate':
                #print 'ROTATE\t' + str(args)
                theta = float(c[2]) * (math.pi / 180)
                if c[1] == 'x':
                    t = make_rotX(theta)
                elif c[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]

            elif line == 'push':
                systems.append( [x[:] for x in systems[-1]] )

            elif line == 'pop':
                systems.pop()

            elif line == 'display' or line == 'save':
                if line == 'display':
                    display(screen)
                else:
                    save_extension(screen, c[0]+c[1])
    else:
        print "Parsing failed."
        return

#run("test.mdl")
#run("robot.mdl")
