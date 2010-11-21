import pygame

from _game_constants import *

import screen

from _buildings import *

import networking
import gui

class ColonyBuildScreen(screen.Screen):

    def __init__(self):
        screen.Screen.__init__(self)

    def reset_triggers_list(self):
        screen.Screen.reset_triggers_list(self)
        self.add_trigger({'action': "ESCAPE", 'hover_id': "ESCAPE", 'rect': pygame.Rect((496, 448), (56, 16))})

    def draw(self, star, planet, colony):
        DISPLAY = gui.GUI.get_display()

        RULES = networking.Client.rules()
        PROTOTYPES = networking.Client.list_prototypes()
        ME = networking.Client.get_me()

        font3 = gui.GUI.get_font('font3')
        font4 = gui.GUI.get_font('font4')
        font5 = gui.GUI.get_font('font5')

        production_palette = [0x0, 0x440c00, 0xac542c]
        xship_palette = [0x0, 0x802810, 0xe48820, 0xe46824]
        build_queue_palette = [0x0, 0x802810, 0xe48820]

        light_text_palette = [0x0, 0x802810, 0xe48820, 0xe46824]
        dark_text_palette = [0x0, 0x440c00, 0xac542c]


        DISPLAY.blit(self.get_image('background', 'starfield'), (0, 0))
#        colony_screen.draw_planet_background(GUI, DISPLAY, IMAGES, PALETTES, planet.get_terrain(), planet.get_picture())
        DISPLAY.blit(gui.GUI.get_planet_background(planet.get_terrain(), planet.get_picture()), (0, 0))

        shadow = pygame.Surface((640, 480))

    #    shadow.fill((0, 0, 0))
    #    shadow.fill((8, 8, 20))
        shadow.fill((28, 32, 44))
        shadow.set_alpha(128)
        DISPLAY.blit(shadow, (0, 0))

    #    c1 = (0, 0, 0, 128)
    #    c1 = (8, 8, 20, 128)
        c1 = (28, 32, 44, 128)

        for y in range(0, 480, 2):
            pygame.draw.line(DISPLAY, c1, (0, y), (639, y), 1)

    #    for x in range(0, 640, 2):
    #        pygame.draw.line(DISPLAY, c1, (x, 0), (x, 479), 1)

#        DISPLAY.blit(IMAGES['COLONY_BUILD_SCREEN']['screen'], (0, 0))
        DISPLAY.blit(self.get_image('colony_build_screen', 'panel'), (0, 0))

    #    buildings = colony.list_buildings()
        print("")
        print("=== Available Production: ===")
        available_production = colony.get_available_production()

        # hack Trade Goods to the first position in list
        if 254 in available_production['building']:
            i = available_production['building'].index(254)
            available_production['building'].pop(i)
        available_production['building'].insert(0, 254)

        # hack Housing to the second position in list
        if 253 in available_production['building']:
            i = available_production['building'].index(253)
            available_production['building'].pop(i)
        available_production['building'].insert(1, 253)

        # hack Freighter Fleet to the first position in list
        if 214 in available_production['xship']:
            i = available_production['xship'].index(214)
            available_production['xship'].pop(i)
            available_production['xship'].insert(0, 214)

        print(available_production)

        y = 20
#        for building_id, building in available_buildings.items():
	# limit listing to 25 items here, overflow causes crash on Solaris, Python 2.6.5, Pygame 1.8.1
        for production_id in available_production['building'][:25]:
            print("production_id = %i" % production_id)
            production_name = RULES['buildings'][production_id]['name']
            print(production_id, production_name)
            font3.write_text(DISPLAY, 13, y, production_name, dark_text_palette, 2)
            hover_id = "production:%i" % production_id
            self.add_trigger({'action': "production", 'production_id': production_id, 'hover_id': hover_id, 'rect': pygame.Rect((13, y), (170, 12))})
            y += 18
        print("=== /Available Buildings ===")
        print("")

        # xships = Freighter Fleet, Colony Ship, Outpost Ship and Transport Ship
        y = 20
        for production_id in available_production['xship']:
            print("production_id = %i" % production_id)
            production_name = RULES['buildings'][production_id]['name']
            print(production_id, production_name)
            font5.write_text(DISPLAY, 485, y, production_name, light_text_palette, 2)
            hover_id = "production:%i" % production_id
            self.add_trigger({'action': "production", 'production_id': production_id, 'hover_id': hover_id, 'rect': pygame.Rect((485, y), (143, 15))})
            y += 19

        print("=== Build Queue ===")
        build_queue = colony.get_build_queue()
        print(build_queue)

        label = font4.render("Build List for %s" % colony.get_name(), light_text_palette, 2)
        DISPLAY.blit(label, (240, 311))

        y = 334
        i = 0
        repeat = False
        for build_item in build_queue:
            production_id = build_item['production_id']
            if production_id < 0xFF:
                if RULES['buildings'][production_id].has_key('type') and RULES['buildings'][production_id]['type'] == "repeat":
                    repeat = True
                    continue

                production_name = RULES['buildings'][production_id]['name']
                label = font4.render(production_name, light_text_palette, 2)
                xx = (250 - label.get_width()) / 2
                DISPLAY.blit(label, (208 + xx, y))
                hover_id = "queue:%i" % i
                if repeat:
                    self.add_trigger({'action': "delete_repeat_production", 'item': i, 'hover_id': hover_id, 'rect': pygame.Rect((208, y - 1), (250, 15))})
                    y += 20
                    label = font4.render("^ Repeat ^", light_text_palette, 2)
                    xx = (250 - label.get_width()) / 2
                    DISPLAY.blit(label, (208 + xx, y))
                    self.add_trigger({'action': "delete_repeat_production", 'item': i, 'hover_id': hover_id, 'rect': pygame.Rect((208, y - 1), (250, 15))})
                    repeat = False
                else:
                    self.add_trigger({'action': "delete_production", 'item': i, 'hover_id': hover_id, 'rect': pygame.Rect((208, y - 1), (250, 15))})
                y += 20
            i += 1

        print("=== /Build Queue ===")

        self.flip()
        return

        print("")
        print("=== Prototypes: ===")
        yy = 0
        for i in range(5):
            prototype = PROTOTYPES[i]
            print("")
            print(prototype)
            print("")
            label_surface = FONTS['font_14_bold'].render(prototype['name'], 1, (0xE4, 0x88, 0x20))
            yy += 19
            DISPLAY.blit(label_surface, (484, 110 + yy))
        print("=== /Prototypes ===")
        print("")

        build_queue = colony.build_queue()
        yy = 0
        print("")
        print("=== Build Queue: ===")
        for queue_item in build_queue:
            print(queue_item)
            build_id = queue_item['item']
            if build_id <  255:
                if build_id == 150:
                    label = PROTOTYPES[0]['name']
                elif build_id == 148:
                    label = PROTOTYPES[1]['name']
                elif build_id == 147:
                    label = PROTOTYPES[2]['name']
                elif build_id == 145:
                    label = PROTOTYPES[3]['name']
                elif build_id == 144:
                    label = PROTOTYPES[4]['name']
                else:
                    label = BUILDINGS[build_id]['name']

                label_surface = FONTS['font_12_bold'].render(label, 1, (0xE4, 0x88, 0x20))
                xx = label_surface.get_width() // 2
                DISPLAY.blit(label_surface, (208 + 126 - xx, 332 + yy))
                yy += 20
        print("=== /Build Queue: ===")
        print("")

        pygame.display.flip()



    # end func draw

    #
    #       RUN
    #
    def run(self, colony_id):
        colony = networking.Client.get_colony(colony_id)

        planet_id = colony.get_planet_id()
        planet = networking.Client.get_planet(planet_id)

        star_id	= planet.get_star()
        star = networking.Client.get_star(star_id)

        self.draw(star, planet, colony)

        while True:
            event = self.get_event()
            if event:
                action = event['action']

                if action == "ESCAPE":
                    return

                if action == "hover":
                    print("hover = %s" % event['hover'])



Screen = ColonyBuildScreen()