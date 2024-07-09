# GlowScript 2.7 VPython
# from visual import *


# scene.bind('keydown', keydown_fun)     # Function for key presses
# scene.background = (1/255)*vector(5, 12, 56) 
# scene.width = 1200                      # Make the 3D canvas larger
# scene.height = 500
# # These functions create "container" objects, called "compounds"


# def make_character(starting_position, starting_vel = vector(0, 0, 0)):
#     """Makes the main character, Io!
#     """
#     character_body = ellipsoid(pos=vector(0,1,0),
#           length=1, height=2.3, width=1, color=(1/255)*vector(73, 138, 138))
#     character_head = sphere(size = vector(1, 1, 1), pos = vector(0, 2.3, 0), color = (1/255)*vector(194, 163, 97)) 
#     character_eye1 = sphere(size = 0.2*vector(1, 1, 1), pos = vector(.35, 2.4, -.2), color = color.black)
#     character_eye2 = sphere(size = 0.2*vector(1, 1, 1), pos = vector(.35, 2.4, .2), color = color.black)
#     character_objects = [character_body, character_head, character_eye1, character_eye2]
#     com_character = compound(character_objects, pos = starting_position)
#     com_character.vel = starting_vel    # set the initial velocity
#     com_character.pos = starting_position
#     return com_character

# def make_tent_w_char(starting_position, starting_vel = vector(0, 0, 0)):
#     """Makes a tent with a character sleeping"""
#     tent = make_tent(starting_position, starting_vel = vector(0, 0, 0))
#     tent.pos = vector(0,0,0)
#     tent.axis = vector(1,0,-1)
#     character = make_character(starting_position, starting_vel = vector(0, 0, 0))
#     character.pos.x = tent.pos.x
#     character.pos.z = tent.pos.z
#     character.pos.y = -.2
#     character.vel = vector(0,0,0)
#     character.axis = vector(-1,-1.7,-1)
#     tent_w_char_objects = [tent, character]
#     com_tent_w_char = compound(tent_w_char_objects, pos = starting_position)
#     com_tent_w_char.vel = starting_vel
#     com_tent_w_char.pos = starting_position
#     return com_tent_w_char
    
# def make_fishing(starting_position, starting_vel = vector(0, 0, 0)):
#     """Makes a fishing pole"""
#     part1 = cylinder(pos = vector(0,-1.8,0), axis = vector(1, 1, 0), size = vector(2.1,.15,.15), color =(1/255)*vector(97, 79, 39))
#     part2 = cylinder(pos = vector(1.4,-.3,0), axis = vector(1.4,-2,0), size =vector(3,.05,.05), color =(1/255)*vector(145, 145, 145))
#     part3 = cylinder(pos = vector(.2,-1.5,0), axis = vector(1, 1, 0), size = vector(.5,.3,.3), color =(1/255)*vector(97, 79, 39))
#     fishing_objects = [part1, part2,part3]
#     com_fishing = compound(fishing_objects, pos = starting_position)
#     com_fishing.vel = starting_vel    # set the initial velocity
#     com_fishing.pos = starting_position
#     return com_fishing
    
# def make_owl(starting_position, starting_vel = vector(0, 0, 0)):
#     """The lines below make a new "frame", which is a container with a
#        local coordinate system.
#        The arguments to make_owl allow for any initial starting position
#        and initial starting velocity, with a default starting velocity
#        of vector(0, 0, 0).

#        Compounds can have any number of components.  Here are the
#        alien's components:
#     """
#     owl_body = ellipsoid(pos=vector(0,.34,0),
#           length=.8, height=1, width=.8, color = (1/255)*vector(153, 133, 103))
#     owl_wing1 = ellipsoid(pos=vector(-.36,.34,-.1),axis=vector(1,1,0), length=.7, height=.2, width=.5, color = (1/255)*vector(107, 88, 60))
#     owl_wing2 = ellipsoid(pos=vector(.36,.34,-.1),axis=vector(-1,1,0), length=.7, height=.2, width=.5, color = (1/255)*vector(107, 88, 60))
#     owl_eye1 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(-.2, 1, .25), color = color.black)
#     owl_eye2 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(.2, 1, .25), color = color.black)
#     owl_head = sphere(pos=vector(0,.8,0), radius = 0.35, color = (1/255)*vector(153, 133, 103))
#     owl_beak = cone(pos = vector(0,.9,.3), axis = vector(0, 0, 1), size = vector(.2,.2,.2), color =(1/255)*vector(107, 88, 60))
#     # make a list to "fuse" with a compound
#     owl_objects = [owl_body, owl_wing1, owl_wing2, owl_eye1, owl_eye2,owl_head,owl_beak]
#     # now, we create a compound -- we'll name it com_alien:
#     com_owl = compound(owl_objects, pos = starting_position)
#     com_owl.vel = starting_vel    # set the initial velocity
#     return com_owl

# def make_flower(starting_position, starting_vel = vector(0,0,0)):
#     """Makes a flower with a random petal color
#     """
#     stem = cylinder(pos = vector(0,-.7,0), axis = vector(0, 1, 0), size = vector(.7,.05,.05), color =(1/255)*vector(86, 140, 92))
#     petals = sphere(pos = vector(0,0,0), size = vector (.2,.05,.2), color=(1/255)*choice([vector(145, 95, 173),vector(146, 174, 214), vector(251, 255, 179)]))
#     flower_objects = [petals,stem]
#     com_flower = compound(flower_objects, pos = starting_position, vel = starting_vel)   
#     return com_flower
    
    
# def make_tent(starting_position=vector(0,0,0), starting_vel=vector(0,0,0)):   
#     """Makes a tent
#     """
#     tent_body = extrusion(path=[vec(-1,0,0), vec(1,0,0)], shape=[shapes.triangle(length=2.7),shapes.triangle(length=2.4)],color=(1/255)*vector(252, 177, 3))
#     return tent_body
    
# def make_bunny(starting_position, starting_vel = vector(0, 0, 0)):
#     """The lines below make a new "frame", which is a container with a
#        local coordinate system.
#        The arguments to make_bunny allow for any initial starting position
#        and initial starting velocity, with a default starting velocity
#        of vector(0, 0, 0).

#        Compounds can have any number of components.  Here are the
#        alien's components:
#     """
#     bunny_body = ellipsoid(pos=(.7)*vector(.5,1,0),
#           length=(.7)*1, height=(.7)*1, width=(.7)*1)
#     bunny_head = sphere(size = (.7)*vector(1, 1, 1), pos = (.7)*vector(.8, 1.5, 0), color = color.white) 
#     bunny_ear1 = ellipsoid(pos=(.7)*vector(.8,1.8,.15),axis=vector(0,1,0), length=(.7)*1.4, height=(.7)*.5, width=(.7)*.4)
#     bunny_ear2 = ellipsoid(pos=(.7)*vector(.8,1.8,-.15),axis=vector(0,1,0), length=(.7)*1.4, height=(.7)*.5, width=(.7)*.4)
#     bunny_eye1 = sphere(size = 0.1*(.7)*vector(1, 1, 1), pos = (.7)*vector(1.25, 1.6, .2), color = color.black)
#     bunny_eye2 = sphere(size = 0.1*(.7)*vector(1, 1, 1), pos = (.7)*vector(1.25, 1.6, -.2), color = color.black)
#     bunny_tail = sphere(size = 0.4*(.7)*vector(1, 1, 1), pos = (.7)*vector(0, 1, 0), color = color.white)
#     # make a list to "fuse" with a compound
#     bunny_objects = [bunny_body, bunny_ear1, bunny_ear2, bunny_head, bunny_eye1, bunny_eye2, bunny_tail]
#     # now, we create a compound -- we'll name it com_alien:
#     com_bunny = compound(bunny_objects, pos = starting_position)
#     com_bunny.vel = starting_vel    # set the initial velocity
#     return com_bunny

# def make_fish(starting_position = vector(0,0,0), starting_vel = vector(0,0,0)):
#     """Makes a fish"""
#     fish_body = sphere(size = vector(.2,.4,.65), pos = vector(0,0,0), color =  (1/255)*vector(235, 167, 66))
#     fish_eye1 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(.1, 0, -.1), color = color.black)
#     fish_eye2 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(-.1, 0, -.1), color = color.black)
#     fish_tail = cone(pos = vector(0,0,.6), axis = vector(0, 0, -1), size = (.4)*vector(1,1,.2), color =(1/255)*vector(235, 167, 66))
#     fish_objects = [fish_body, fish_eye1, fish_eye2, fish_tail]
#     com_fish = compound(fish_objects, pos = starting_position)
#     return com_fish

# def make_cookedfish(starting_position = vector(0,0,0), starting_vel = vector(0,0,0)):
#     """Makes a cooked fish"""
#     cookedfish_body = sphere(size = vector(.2,.4,.65), pos = vector(0,0,0), color =  (1/255)*vector(145, 128, 80))
#     cookedfish_eye1 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(.1, 0, -.1), color = color.black)
#     cookedfish_eye2 = sphere(size = 0.1*vector(1, 1, 1), pos = vector(-.1, 0, -.1), color = color.black)
#     cookedfish_tail = cone(pos = vector(0,0,.6), axis = vector(0, 0, -1), size = (.4)*vector(1,1,.2), color =(1/255)*vector(145, 128, 80))
#     cookedfish_objects = [cookedfish_body, cookedfish_eye1, cookedfish_eye2, cookedfish_tail]
#     com_cookedfish = compound(cookedfish_objects, pos = starting_position)
#     return com_cookedfish
    
# def make_tree(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0)):
#     """Makes a tree
#     """
#     stump = cylinder(pos = vector(0,3,0), axis = vector(0, 1, 0), size = vector(4,1.2,1.2), color =(1/255)*vector(97, 79, 39))
#     leaves = cone(pos = vector(0,6,0), axis = vector(0,1,0), size = vector (3,4,3), color=(1/255)*vector(84, 156, 86))
#     tree_objects = [stump,leaves]
#     com_tree = compound(tree_objects, pos = starting_position)   
#     return com_tree

# def make_bush(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     """The lines below make a new bush
#     """
#     leaf1 = sphere(pos = vector(.3,0,0), axis = vector(0, 1, 0), size = vector(1,1,1), color =(1/255)*vector(84, 156, 86))
#     leaf2 = sphere(pos = vector(0,0,0), axis = vector(0, 1, 0), size = vector(1,1,1), color =(1/255)*vector(84, 156, 86))
#     leaf3 = sphere(pos = vector(0,.5,0), axis = vector(0, 1, 0), size = vector(1,1,1), color =(1/255)*vector(84, 156, 86))
#     leaf4 = sphere(pos = vector(.3,0,.3), axis = vector(0, 1, 0), size = vector(1,1,1), color =(1/255)*vector(84, 156, 86))
#     leaf5 = sphere(pos = vector(0,0,.3), axis = vector(0, 1, 0), size = vector(1,1,1), color =(1/255)*vector(84, 156, 86))
#     bush_objects = [leaf1,leaf2,leaf3,leaf4,leaf5]
#     com_bush = compound(bush_objects, pos = starting_position)   
#     return com_bush

# def make_beforefire(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     """Makes a fire before the fire is lit
#     """
#     lg1 = cylinder(pos = vector(0,0,0), axis = vector(1, 2, 1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))
#     lg2 = cylinder(pos = vector(1,0,0), axis = vector(-1, 2, 1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))
#     lg3 = cylinder(pos = vector(.7,0,1.3), axis = vector(0, 2, -1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))    
#     beforefire_objects = [lg1,lg2,lg3]
#     com_beforefire = compound(beforefire_objects, pos=starting_position)
#     return com_beforefire
    
# def make_afterfire(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     """Makes a burning fire
#     """
#     lg1 = cylinder(pos = vector(0,0,0), axis = vector(1, 2, 1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))
#     lg2 = cylinder(pos = vector(1,0,0), axis = vector(-1, 2, 1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))
#     lg3 = cylinder(pos = vector(.7,0,1.3), axis = vector(0, 2, -1), size = vector(2,.5,.5), color =(1/255)*vector(97, 79, 39))  
#     flame1 = ellipsoid(pos=vector(.5,1.8,.8),
#           length=.35, height=1, width=.35, color=(1/255)*vector(247, 223, 35)) 
#     flame2 = ellipsoid(pos=vector(.4,1.7,.5),
#           length=.35, height=1.3, width=.35, color=(1/255)*vector(196, 98, 18)) 
#     flame3 = ellipsoid(pos=vector(.5,2,.5),
#           length=.35, height=1.4, width=.35, color=(1/255)*vector(235, 165, 16)) 
#     flame4 = ellipsoid(pos=vector(.6,1.8,.3),
#           length=.35, height=1.2, width=.35, color=(1/255)*vector(201, 162, 4)) 
#     flame5 = ellipsoid(pos=vector(.8,1.8,.5),
#           length=.35, height=1.2, width=.35, color=(1/255)*vector(212, 124, 23)) 
#     beforefire_objects = [lg1,lg2,lg3,flame1,flame2,flame3,flame4,flame5]
#     com_beforefire = compound(beforefire_objects, pos=starting_position)
#     return com_beforefire

# def make_note(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     """Makes a small note"""
#     note = extrusion(path=[vec(0,-.05,0), vec(0,0,0)],
#     color=(1/155)*vector(252,251,227),
#     shape=[shapes.rectangle(length=.4, width=.4)])
#     return note

# def make_tentscrap(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     """Makes a small tent scrap"""
#     tentscrap = extrusion(path=[vec(0,-.05,0), vec(0,0,0)],
#     color=(1/155)*vector(252, 177, 3),
#     shape=[shapes.rectangle(length=1, width=1)])
#     return tentscrap

# def make_satan(starting_position = vector(0,0,0), starting_vel = vector(0, 0, 0) ):
#     satan_body = ellipsoid(pos=vector(0,1,0),
#           length=1, height=2.3, width=1, color=(1/255)*vector(102,0,0))
#     satan_head = sphere(size = vector(1, 1, 1), pos = vector(0, 2.3, 0), color = (1/255)*vector(204,0,0)) 
#     satan_eye1 = sphere(size = 0.2*vector(1, 1, 1), pos = vector(.35, 2.4, -.2), color = color.white)
#     satan_eye2 = sphere(size = 0.2*vector(1, 1, 1), pos = vector(.35, 2.4, .2), color = color.white)
#     satan_horn1 = cone(pos = vector(0,2.6,.3), axis = vector(0,1,1), size = vector (.3,.3,.3), color=color.white)
#     satan_horn2 = cone(pos = vector(0,2.6,-.3), axis = vector(0,1,-1), size = vector (.3,.3,.3), color=color.white)
#     satan_objects = [satan_body, satan_head, satan_eye1, satan_eye2, satan_horn1, satan_horn2]
#     com_satan = compound(satan_objects, pos = starting_position)
#     com_satan.vel = starting_vel    # set the initial velocity
#     com_satan.pos = starting_position
#     return com_satan
    

# ground = extrusion(path=[vec(0,-.5,0), vec(0,-1.5,0)],
#     color=color.black,
#     shape=[shapes.rectangle(length=30, width=30),shapes.circle(radius=3, pos = [0,10])], color = (1/255)*vector(52, 89, 46))
# water = cylinder(pos = vector(-10,-1,0), axis = vector(0,-1,0), size = vector (.5,6,6), color = (1/255)*vector(22, 90, 145))



# wallA = box(pos = vector(0, 0, -15), axis = vector(1, 0, 0), size = vector(30, 1, .2), color = (1/255)*vector(97, 79, 39)) 
# wallB = box(pos = vector(-15, 0, 0), axis = vector(0, 0, 1), size = vector(30, 1, .2), color = (1/255)*vector(97, 79, 39))   
# wallC = box(pos = vector(0, 0, 15), axis = vector(1, 0, 0), size = vector(30, 1, .2), color = (1/255)*vector(97, 79, 39)) 
# wallD = box(pos = vector(15, 0, 0), axis = vector(0, 0, 1), size = vector(30,1,.2), color = (1/255)*vector(97, 79, 39))   

# # +++ start of OBJECT_CREATION section

# flower1 = make_flower(starting_position = vector(-12,-.7,10), starting_vel=vector(0,0,0))
# flower2 = make_flower(starting_position = vector(-13,-.7,10.7), starting_vel=vector(0,0,0))
# flower3 = make_flower(starting_position = vector(-12.8,-.7,10), starting_vel=vector(0,0,0))
# flower4 = make_flower(starting_position = vector(-12,-.7,10.5), starting_vel=vector(0,0,0))
# flower5 = make_flower(starting_position = vector(-12.2,-.7,9.6), starting_vel=vector(0,0,0))
# flower6 = make_flower(starting_position = vector(-12.8,-.7,11), starting_vel=vector(0,0,0))
# flower7 = make_flower(starting_position = vector(-12.5,-.7,10.4), starting_vel=vector(0,0,0))
# character = make_character(starting_position = vector(.1,0,10), starting_vel=vector(0,0,0))
# character.axis = vector(0,0,1)
# character.pos = vector(.1,0,10)
# bunny = make_bunny(starting_position = vector(2, 1.5, -7), starting_vel = vector(2, -1, -2))
# tree1 = make_tree(starting_position = vector(-10,2,10),starting_vel = vector(0, 0, 0))
# tree1.vel = vector(0,0,0)
# tree2 = make_tree(starting_position = vector(.1,2,.1),starting_vel = vector(0, 0, 0))
# tree2.vel = vector(0,0,0)
# tree3 = make_tree(starting_position = vector(-7,2,-7),starting_vel = vector(0, 0, 0))
# tree3.vel = vector(0,0,0)
# tree4 = make_tree(starting_position = vector(10,2,-10),starting_vel = vector(0, 0, 0))
# tree4.vel = vector(0,0,0)
# bush1 = make_bush(starting_position = vector(-5,0,6),starting_vel = vector(0, 0, 0))
# bush1.vel = vector(0,0,0)
# bush2 = make_bush(starting_position = vector(5,0,-6),starting_vel = vector(0, 0, 0))
# bush2.vel = vector(0,0,0)
# beforefire = make_beforefire(starting_position = vector(10,0,6),starting_vel = vector(0, 0, 0))
# beforefire.vel = vector(0,0,0)
# owl = make_owl(starting_position = vector(-8,4,11), starting_vel = vector(0, .3, 0))
# owl.vel = vector(0,.5,0)
# owl.pos = vector(-8,4,11)
# owl.visible = False
# note= make_note(starting_position = vector(-8,6,11), starting_vel = vector(0,0,0))
# note.pos = vector(-8,4.5,12)
# note.vel = vector(0,0,0)
# note.visible = False
# fish = make_fish(starting_position = vector(7,3,11), starting_vel = vector(0,0,0))
# fish.pos = vector(-10,-1,-2)
# fish.vel = vector(.1,0,.9)
# rock1 = sphere(pos = vector(-11, -.5, -11), size=vector(2,1,2), color = (1/255)*vector(107, 102, 95))
# rock1.vel = vector(0,0,0)
# rock2 = sphere(pos = vector(-10, 0, -11), size=vector(2,1,1), axis = vector(-1,1,0), color = (1/255)*vector(56, 53, 49))
# rock2.vel = vector(0,0,0)
# fishingrod = make_fishing(starting_position =vector(0,0,0), starting_vel = vector(0,0,0))
# fishingrod.vel = vector(0,0,0)
# fishingrod.visible = False
# cookedfish = make_cookedfish(starting_position = vector(0,0,0), starting_vel = vector(0,0,0))
# cookedfish.pos = vector(10.2,1.6,6)
# cookedfish.axis = vector(1,1,0) 
# cookedfish.visible = False
# tentscrap = make_tentscrap(starting_position = vector(0,0,0), starting_vel = vector(0,0,0))
# tentscrap.pos = vector(-10.3,-.48,-10.3)
# tentscrap.vel = vector(0,0,0)
# tentscrap.visible = True
# tent = make_tent()
# tent.pos = vector(-10.3,-.48,-10.3)
# tent.vel = vector(0,0,0)
# tent.visible = False
# tent2 = make_tent()
# tent2.pos = vector(-10.3,-.48,-10.3)
# tent2.vel = vector(0,0,0)
# tent2.visible = False
# tent_w_char = make_tent_w_char(starting_position = vector(0,0,0), starting_vel = vector(0,0,0))
# tent_w_char.pos = vector(0,0,0)
# tent_w_char.vel = vector(0,0,0)
# tent_w_char.visible = False
# satan = make_satan(starting_position = vector(0,0,0), starting_vel = vector(0,0,0))
# satan.pos = vector(1,0,-11)
# satan.vel = 2*vector(2,0,10)
# satan.visible = False
# afterfire = make_afterfire(starting_position = vector(10,0.5,6))
# afterfire.vel = vector(0,0,0)
# afterfire.visible = False
# #character.color = color.black
# # +++ end of OBJECT_CREATION section

# # Other constants
# RATE = 30                # The number of times the while loop runs each second
# dt = 1.0/(1.0*RATE)      # The time step each time through the while loop
# scene.autoscale = False  # Avoids changing the view automatically
# scene.forward = vector(0, -.8, -2)  # Ask for a bird's-eye view of the scene...

# MM=[0] #If 0, no tent has been placed. Keeps you from placing more than one tent
# LL = [tree1, tree2, tree3, tree4, bush1, bush2, beforefire, afterfire, bunny,rock1,rock2,fishingrod, tent_w_char] #List without character
# NN = [tree1, tree2, tree3, tree4, bush1, bush2, beforefire, afterfire, bunny, character, rock1, rock2, fishingrod, tent_w_char]
# b = [0]
# # +++ start of ANIMATION section

# # This is the "event loop" or "animation loop"
# # Each pass through the loop will animate one step in time, dt
# #
# # +++ start of EVENT_HANDLING section -- separate functions for
# #                                keypresses and mouse clicks...
# def keydown_fun(event):
#     """This function is called each time a key is pressed. Actions are key specific. See further comments below"""
#     key = event.key
#     ri = randint(0, 10)
#     amt = 0.4              # "Strength" of the keypress's velocity changes
#     if key == 'up' or key in 'wWiI':
#         character.vel = .8*character.vel + vector(0, 0, -amt)
#     elif key == 'left' or key in 'aAjJ':
#         character.vel = .8*character.vel + vector(-amt, 0, 0)
#     elif key == 'down' or key in 'sSkK':
#         character.vel = .8*character.vel + vector(0, 0, amt)
#     elif key == 'right' or key in "dDlL":
#         character.vel = .8*character.vel + vector(amt, 0, 0)
#     elif key == 'shift' or key in "xXmM":
#         character.vel *= .01
#     elif key == 'ctrl':
#         if mag(character.vel) < 8:
#             character.vel *= 1.5
#     elif key in 'rR':
#         character.vel = vector(0, 0, 0) 
#         character.pos = vector(0,0,10)
#     elif key in ' ':
#         """Lights fire if close to fire. Reveals owl if close to tree1"""
#         if b[0] == 0:
#             if mag(character.pos - beforefire.pos) < 4:
#                 print("")
#                 print("What a nice fire! And look! The sky is a bit brighter!")
#                 print("I'm a quite hungry, though. I wonder where I can find some food to cook on the fire...")
#                 print("Do you think that pond might have any fish? We should go check it out! When we arrive, press space.")
#                 scene.background= (1/255)*vector(40,70,121)
#                 beforefire.visible = False
#                 afterfire.visible = True
#             if mag(character.pos - tree1.pos) < 4:
#                 print("Wow! It's an owl!")
#                 owl.visible = True
#                 print("Did she drop a note?")
#                 print("")
#                 note.visible = True
#                 note.vel.y = -2.5
#                 print("It says, 'Burn a fire to bring light to the sky. Press space when you are nearby.'")
#             if sqrt((character.pos.x+10)**2 + (character.pos.z)**2) < 3:
#                 print("Ahh! I've fallen into the water! Can you help me get out?")
#             if 5 > sqrt((character.pos.x+10)**2 + (character.pos.z)**2) > 3:
#                 print("Here we are!")
#                 print("Press F to fish!")
#         if b[0] == 3:
#             if mag(character.pos-bunny.pos) < 3:
#                 b[0]=4
#                 bunny.vel = vector(0,0,0)
#                 bunny.pos.y=0
#                 print("Hi there, bunny. Do you know how to make the sky light again?")
#                 print("")
#                 print("She says to sleep. Apparently, if I go to bed, it'll be daytime when I wake up. What a strange concept.")
#                 print("I guess I'd better find a tent! I thought I saw a piece of orange fabric around here somewhere. Could that be it? Press space if you find it.")
#                 b[0]=4
#         if b[0] == 1:
#             """Cooks fish"""
#             cookedfish.visible = True
#             fish.visible = False
#             print("")
#             print("That fish looks good! Thanks for helping me catch it! Press E and I'll eat the fish! Then we can keep bringing light to the sky!")
#             character.pos = vector(8,0,6)
#             b[0] = 2
#         if mag(character.pos-rock1.pos) < 2.5:
#             """Lets you pick up tent scrap"""
#             if b[0] == 4:
#                 tentscrap.visible = False
#                 print("")
#                 print("Got it! Thanks so much! Now, we just have to place the tent. Press T when you've chosen your spot.")
#                 b[0] = 5
#     elif key in "Ee":
#         """Lets you eat the fish if it's cooked"""
#         if b[0] == 2:
#             cookedfish.visible = False
#             print("")
#             print("That tasted great! Hey, what if we chat with the bunny over there? She might be able to tell us something. We just have to catch her first! Press space when you reach her.")
#             print("")
#             b[0] = 3
#     elif key in "fF":
#         """Lets you cast a fishing rod"""
#         if 5 > sqrt((character.pos.x+10)**2 + (character.pos.z)**2) > 3:
#             fishingrod.visible = True
#             fishingrod.pos = vector(-6.5,0,0)
#             fishingrod.axis = vector(-1,0,0)
#             if mag(fishingrod.pos-character.pos) < 3:
#                 fishingrod.pos = vector(-10,0,2.5)
#                 fishingrod.axis = vector(0,0,-1)
#             print("The fishing rod is all set up! Press C when the fish is nearby to catch the fish.")
#     elif key in "cC":
#         """Lets you catch a fish if the fish is close enough"""
#         if mag(fish.pos-fishingrod.pos)<2.4:
#             fish.vel = vector(0,0,0)    
#             print("Nice! You caught it! Press space and I'll put it on the fire for us to eat!")
#             b[0] = 1
#     elif key in "tT":
#         """Places tent"""
#         if b[0] == 5:
#             allowed = [0]
#             if MM[0] == 0:
#                 for a in LL:
#                     tent1 = make_tent()
#                     tent1.visible = True
#                     tent1.pos.z = character.pos.z - 1.5 
#                     tent1.pos.x = character.pos.x + 1.5
#                     tent1.pos.y = .6
#                     if tent_collision(tent1, a) == True:
#                         allowed[0] = 1
#                         tent1.visible = False
#                         del tent1
#                     else:
#                         tent1.visible = False
#                         del tent1                       
#                 if allowed[0] == 0:
#                     b[0] = 6
#                     tent.visible = True
#                     tent.pos.z = character.pos.z - 1.5 
#                     tent.pos.x = character.pos.x + 1.5
#                     tent.pos.y = .3
#                     tent.axis = vector(1,0,-1)
#                     tent.vel = vector(0,0,0)
#                     print("")
#                     print("That's one well-assembled tent! Now we just have to sleep. Go near the tent and press Z!")
#                     MM[0] = 1
#                     NN.append(tent)
#                 else:
#                     print("")
#                     print("You can't place a tent here!")
#             else:
#                 print("")
#                 b[0] = 6
#                 print("You only had one tent!")
#     elif key in "zZ":
#         """Sleeps if near tent"""
#         if b[0]==6:
#             if mag(character.pos - tent.pos) < 3:
#                 b[0] = 7
#                 print("Let's sleep!")
#                 character.visible = False
#                 tent_w_char.pos = tent.pos
#                 tent.visible = False                
#                 tent_w_char.visible = True
#     elif key in "7":
#         """Summon satan"""
#         b[0] = 11
#         print("Oh no! You've summoned Satan! I'm toast!")
        
    
    

# # +++ End of EVENT_HANDLING section


# # +++ Other functions can go here...

# def choice(L):
#     """Implements Python's choice using the random() function."""
#     LEN = len(L)                        # Get the length
#     randomindex = int(LEN*random())     # Get a random index
#     return L[randomindex]               # Return that element

# def randint(low, hi):
#     """Implements Python's randint using the random() function.
#        returns an int from low to hi _inclusive_ (so, it's not 100% Pythonic)
#     """
#     if hi < low:
#         low, hi = hi, low               # Swap if out of order!
#     LEN = int(hi) - int(low) + 1.       # Get the span and add 1
#     randvalue = LEN*random() + int(low) # Get a random value
#     return int(randvalue)               # Return the integer part of it

# def collision(one, two):
#     """Tells you when two objects collide. Arguments are two objects with velocities and positions.
#        Returns True if they're colliding. Else returns False.
#     """
#     if mag(vector(one.pos.x,0,one.pos.z) - vector(two.pos.x,0,two.pos.z)) < 1.5:
#         return True
#     else:
#         return False
        
# def notcollision(one, two):
#     """Tells you when two objects are really far from colliding. Arguments are two objects with velocities and positions.
#        Returns True if they're over 2.3 units from colliding. Else returns False.
#     """
#     if mag(vector(one.pos.x,0,one.pos.z) - vector(two.pos.x,0,two.pos.z)) > 2.3:
#         return True
#     else:
#         return False
        
# def tent_collision(tent, other):
#     """Tells you if tent (argument 1) is colliding with another object (argument 2). 
#        Returns true if they're colliding. Else returns false.
#     """
#     if mag(vector(tent.pos.x,0,tent.pos.z) - vector(other.pos.x,0,other.pos.z)) < 1.5:
#         return True
#     else:
#         return False


# def corral_collide(ball):
#     """Corral collisions! Makes sure moving objects stay within walls. If they hit walls, their velocities will be multiplied by -1/
#        Ball must have a .vel field and a .pos field.
#     """
#     if ball.pos.z < wallA.pos.z:           # Hit -- check for z
#         ball.pos.z = wallA.pos.z           # Bring back into bounds
#         ball.vel.z *= -1.0                 # Reverse the z velocity

#     # If the ball hits wallB
#     if ball.pos.x < wallB.pos.x:           # Hit -- check for x
#         ball.pos.x = wallB.pos.x           # Bring back into bounds
#         ball.vel.x *= -1.0                 # Reverse the x velocity

#     if ball.pos.z > wallC.pos.z:           # Hit -- check for z
#         ball.pos.z = wallC.pos.z           # Bring back into bounds
#         ball.vel.z *= -1.0  
# #    
#     if ball.pos.x > wallD.pos.x:           # Hit -- check for x
#         ball.pos.x = wallD.pos.x           # Bring back into bounds
#         ball.vel.x *= -1.0  
    
#     if ball == character:
#         if sqrt((ball.pos.x+10)**2 + (ball.pos.z)**2) < 3:
#             ball.vel.x *= 0.7
#             ball.vel.z *= 0.7
#             ball.pos.y = -1
#         else:
#             ball.pos.y=0
    
#     if ball != character:
#         if sqrt((ball.pos.x+10)**2 + (ball.pos.z)**2) < 4:
#             ball.vel.x *= -1
#             ball.vel.z *= -1
    

# print("Hello there! I'm Io, and this is the Forest. It's nice here, don't you think? (It's nice unless you press 7. Never press 7...)")
# sleep(4)
# print("There's just one issue. The sun has disappeared. It's been nighttime for ages.")
# print("")
# sleep(2)
# print("Let's look around. I thought that tree by the flowers looked peculiar. When you're next to it, try pressing space.")
# print("")


# a = 0 #This is the starting radian value for the fish position


    
# while True:
#     rate(RATE)    
# # maximum number of times per second the while loop runs

#     # +++ Start of PHYSICS UPDATES -- update all positions here, every time step
#     if b[0] < 7: #Before character sleeps
#         character.pos = character.pos + character.vel*dt      
#         if mag(character.vel) > 0:
#             character.axis.z=character.vel.z
#             character.axis.x=character.vel.x

#     if 12>b[0]>7: #After character wakes up, but before Satan catches Io
#         character.pos = character.pos + character.vel*dt      
#         if mag(character.vel) > 0:
#             character.axis.z=character.vel.z
#             character.axis.x=character.vel.x
#         bunny.pos = bunny.pos + bunny.vel*dt
#         if bunny.pos.y < 0:
#             bunny.vel.y*=-1
#         else:
#             bunny.vel.y += -20.8*dt
#         bunny.axis.z=bunny.vel.z
#         bunny.axis.x=bunny.vel.x
#         fish.pos = fish.pos + fish.vel*dt
#         a += pi/5 * dt
#         fish.vel.z = sin(a)
#         fish.vel.x = cos(a)
#         fish.axis.z = fish.vel.x
#         fish.axis.x = -fish.vel.z
    
#     if 12 > b[0]: #Before satan catches Io
#         owl.pos = owl.pos + owl.vel*dt
#         if owl.pos.y > 6:
#             owl.vel.y *= -1
#         if owl.pos.y < 4:
#             owl.vel.y *= -1
    
#     note.pos = note.pos + note.vel*dt #Falling note
#     if note.pos.y < -.48:
#        note.vel.y = 0

#     if b[0] == 0:#Before fish is caught
#         fish.pos = fish.pos + fish.vel*dt
#         a += pi/5 * dt
#         fish.vel.z = sin(a)
#         fish.vel.x = cos(a)
#         fish.axis.z = fish.vel.x
#         fish.axis.x = -fish.vel.z

#     if b[0] < 4:#Before bunny is caught
#         bunny.pos = bunny.pos + bunny.vel*dt
#         if bunny.pos.y < 0:
#             bunny.vel.y*=-1
#         else:
#             bunny.vel.y += -20.8*dt
#         bunny.axis.z=bunny.vel.z
#         bunny.axis.x=bunny.vel.x
    
        
#     if b[0] == 7: #When character falls asleep
#         print("Zzzzzzzzzzzz.........")
#         sleep(4)
#         scene.background = (1/255)*vector(185, 233, 255) 
#         ground.color = color.green
#         sleep(1)
#         tent.visible = True
#         tent_w_char.visible = False
#         character.visible = True
#         print("Ahhhhhhh!!!!! You did it! Thank you so much! It's daytime again! This is wonderful!! You win!!!!!")
#         NN.append(tent)
#         bunny.vel = vector(2, -1, -2)
#         bunny.pos.y = 1.5
#         b[0] = 8
    
#     if b[0] == 8: #After you win!
#         bunny.pos = bunny.pos + bunny.vel*dt
#         if bunny.pos.y < 0:
#             bunny.vel.y*=-1
#         else:
#             bunny.vel.y += -20.8*dt
#         bunny.axis.z=bunny.vel.z
#         bunny.axis.x=bunny.vel.x        

    
    
#     if b[0] == 11:#When satan is called
#         satan.visible = True
#         character.pos = character.pos + character.vel*dt      
#         satan.pos = satan.pos + satan.vel*dt
#         if mag(satan.vel) > 0:
#             satan.axis.z=satan.vel.z
#             satan.axis.x=satan.vel.x
#         if mag(character.vel) > 0:
#             character.axis.z=character.vel.z
#             character.axis.x=character.vel.x
#         aa = [0]
#         for i in range(len(NN)):
#             if collision(NN[i], satan) == True:
#                 (NN[i]).vel *= -1
#                 satan.vel *= -1
#             if notcollision(NN[i], satan) == False:
#                 aa[0]=1
#         if aa[0] == 0:
#             satan.vel = 1.5*(character.pos-satan.pos)/(mag(character.pos-satan.pos))
#         fish.pos = fish.pos + fish.vel*dt
#         a += pi/5 * dt
#         fish.vel.z = sin(a)
#         fish.vel.x = cos(a)
#         fish.axis.z = fish.vel.x
#         fish.axis.x = -fish.vel.z
#         if mag(satan.pos-character.pos) < 2:
#             character.vel = vector(0,0,0)
#             b[0] = 12
        
#     if b[0] == 12: #When Satan catches Io
#         tentscrap.color = color.red
#         wallA.color = (1/255)*vector(160,160,160)
#         wallB.color = (1/255)*vector(160,160,160)
#         wallC.color = (1/255)*vector(160,160,160)
#         wallD.color = (1/255)*vector(160,160,160)
#         note.color = (1/255)*vector(160,160,160)
#         character.color = (1/255)*vector(96,96,96)
#         bunny.color = (1/255)*vector(96,96,96)
#         fish.color = color.black
#         tent.color = color.red
#         beforefire.color = color.red
#         afterfire.color = color.red
#         cookedfish.color = (1/255)*vector(96,96,96)
#         bush1.color = color.red
#         bush2.color = color.red
#         tree1.color = color.red
#         tree2.color = color.red
#         tree3.color = color.red
#         tree4.color = color.red
#         rock1.color = (1/255)*vector(96,96,96)
#         rock2.color = (1/255)*vector(96,96,96)
#         owl.color = (1/255)*vector(96,96,96)
#         flower1.color = (1/255)*vector(160,160,160)
#         flower2.color = (1/255)*vector(160,160,160)
#         flower3.color = (1/255)*vector(160,160,160)
#         flower4.color = (1/255)*vector(160,160,160)
#         flower5.color = (1/255)*vector(160,160,160)
#         flower6.color = (1/255)*vector(160,160,160)
#         flower7.color = (1/255)*vector(160,160,160)
#         fishingrod.color =  (1/255)*vector(160,160,160)
#         water.color = color.red
#         ground.color = color.gray(.3)
#         scene.background = (1/255)*vector(32,32,32)
#         b[0] = 13
#         corral_collide(satan)
#         satan.pos = satan.pos + satan.vel*dt
#         if mag(satan.vel) > 0:
#             satan.axis.z=satan.vel.z
#             satan.axis.x=satan.vel.x
#         for i in range(len(NN)):
#             if collision(NN[i], satan) == True:
#                 satan.vel *= -1  
#                 (NN[i]).vel *= -1
#         if collision(satan, beforefire) == True:
#             satan.vel *= -1          
                  
    
#     if b[0] == 13: #After Satan catches Io
#         print("")
#         print("And now we enter the truly endless night... goodbye, friend.")
#         b[0] = 14
#         corral_collide(satan)
#         satan.pos = satan.pos + satan.vel*dt
#         if mag(satan.vel) > 0:
#             satan.axis.z=satan.vel.z
#             satan.axis.x=satan.vel.x
#         for i in range(len(NN)):
#             if collision(NN[i], satan) == True:
#                 satan.vel *= -1  
#                 (NN[i]).vel *= -1
#         if collision(satan, beforefire) == True:
#             satan.vel *= -1      
                
#     if b[0] == 14: #After Satan catches Io
#         character.vel.y = -.3
#         character.pos.y = character.pos.y + character.vel.y*dt      
#         corral_collide(satan)
#         satan.pos = satan.pos + satan.vel*dt
#         if mag(satan.vel) > 0:
#             satan.axis.z=satan.vel.z
#             satan.axis.x=satan.vel.x
#         for i in range(len(NN)):
#             if collision(NN[i], satan) == True:
#                 satan.vel *= -1  
#                 (NN[i]).vel *= -1
#         if collision(satan, beforefire) == True:
#             satan.vel *= -1    

#     # +++ End of PHYSICS UPDATES -- be sure new objects are updated appropriately!


#     # +++ Start of COLLISIONS -- check for collisions & do the "right" thing

#     if b[0] != 14:
#         corral_collide(character)
#         corral_collide(bunny)
#         corral_collide(satan)
        
#         if collision(satan, beforefire) == True:
#             satan.vel *= -1
            
#         if collision(bunny, beforefire) == True:
#             bunny.vel *= -1
            
#         if collision(character, beforefire) == True:
#             character.vel *= -1
        
#         if mag(fish.pos - character.pos) < 2:
#             if fish.pos.y > -2:
#                 fish.vel.y = -1
#             else:
#                 fish.vel.y =0
#         else:
#             if fish.pos.y < -1:
#                 fish.vel.y = 1
#             else:
#                 fish.vel.y = 0
    
#         for i in range(len(NN)):
#             for j in range(i + 1, len(NN)): # note we start at i + 1
#                 if collision(NN[i], NN[j]) == True:
#                     (NN[i]).vel *= -1
#                     (NN[j]).vel *= -1

    
#     # +++ End of COLLISIONS