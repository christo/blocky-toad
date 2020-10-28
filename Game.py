#!/usr/bin/env python3

# BLOCKY TOAD : like Frogger but instead of a frog it's a toad and instead of a toad it's a block
#
# by ChromoSundrift @chromosundrift
#
# written with python 3.9 | pygame 2.0.0.dev18 | pipenv

import math
import sys

import pygame
from pygame import Rect

import config
from Terrain import Terrain

VERSION = 0.1

PLAYING = 1
TITLE = 2
GET_READY = 3
GAME_OVER = 4
LEVEL_COMPLETE = 5

"""convenience constants; component offsets for tuple coordinates"""
X = 0
Y = 1


# noinspection PyAttributeOutsideInit
class Game:
    """ Main class for running the game """

    def __init__(self):
        # the time until which we may not listen for keyboard controls
        self.obey_controls_at = 0
        # the time at which we go to the title screen
        self.title_at = 0
        # the time at which gameplay starts
        self.play_at = 0
        self.riding = None
        self.goals_reached = []
        self.game_state = TITLE
        self.game_on = True
        self.score = 0
        self.high_score = 0
        self.level_num = config.start_level
        rows = config.levels[self.level_num]["level"]
        self.frog_pos = config.levels[self.level_num]["start"]
        pygame.init()
        self.screen = pygame.display.set_mode((config.width, config.height), pygame.RESIZABLE)
        self.recalculate_sizes(rows)
        self.vehicles = []
        self.lives = config.lives
        self.timer = pygame.time.get_ticks() + config.levels[self.level_num]["time"] * 1000

    def loop(self):
        """Main game loop runs until quit."""
        pygame.display.set_caption(config.game_name + " " + config.byline)
        clock = pygame.time.Clock()

        while self.game_on:
            clock.tick(30)
            self.check_events()
            self.update()
            self.draw()
            pygame.display.flip()

        # game over
        pygame.quit()

    def update(self):
        """Main routine for advancing the game state intended to be called every frame"""
        self.high_score = max(self.score, self.high_score)
        if self.game_state == PLAYING and self.got_all_goals():
            self.next_level()
        elif self.game_state == GET_READY and self.play_at < pygame.time.get_ticks():
            self.game_state = PLAYING
        elif self.game_state == GAME_OVER and self.title_at < pygame.time.get_ticks():
            self.game_state = TITLE
        elif self.game_state == LEVEL_COMPLETE and self.play_at < pygame.time.get_ticks():
            self.get_ready()

        if self.game_state == PLAYING and pygame.time.get_ticks() >= self.timer:
            self.game_state = GAME_OVER
            self.title_at = pygame.time.get_ticks() + 3000

        # update all vehicles
        for v in self.vehicles:
            v.update(self.playfield_wb)
            if v == self.riding:
                new_riding_pos = (self.riding.pos[X] + self.riding_x_offset, self.riding.pos[Y])
                if self.is_on_screen(new_riding_pos):
                    self.frog_pos = new_riding_pos
                elif not v.collides_with(self.frog_pos):
                    # we have fallen off a vehicle
                    self.riding = None
            elif v.collides_with(self.frog_pos):
                # we have a collision with a new vehicle
                if v.rideable:
                    self.riding = v
                    self.riding_x_offset = v.pos[X] - self.frog_pos[X]
                else:
                    if config.debug_mode:
                        print("hit by unrideable %s" % v)
                    self.die()

    def reset_timer(self):
        self.timer = pygame.time.get_ticks() + config.levels[self.level_num]["time"] * 1000 + config.get_ready_timeout

    def check_events(self):
        """React to all pygame events, keys as well as window lifecycle events."""
        for event in pygame.event.get():
            if self.game_state == PLAYING and event.type == pygame.KEYDOWN:
                self.check_controls()
            elif self.game_state == TITLE and event.type == pygame.KEYUP:
                self.start_level()
            if event.type == pygame.QUIT:
                self.game_on = False
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.update()
                self.recalculate_sizes(self.current_level())

    def start_level(self):
        """update all the game state to begin the current level"""
        self.goals_reached = []
        self.reset_vehicles()
        self.reset_frog()
        self.get_ready()
        self.reset_timer()

    def get_ready(self):
        self.game_state = GET_READY
        self.play_at = pygame.time.get_ticks() + config.get_ready_timeout

    def reset_frog(self):
        self.riding = None
        self.frog_pos = config.levels[self.level_num]["start"]

    def reset_vehicles(self):
        self.vehicles = []
        for s in config.levels[self.level_num]["spawns"]:
            self.vehicles.append(s["vehicle"].spawn(s["location"]))

    def check_controls(self):
        """Obeying the controls timeout, check game-playing controls and update game in response"""
        # control the frog by arrow keys or WASD
        key = pygame.key.get_pressed()
        if pygame.time.get_ticks() > self.obey_controls_at:
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.hop((-1, 0))
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.hop((1, 0))
            elif key[pygame.K_UP] or key[pygame.K_w]:
                self.hop((0, -1))
            elif key[pygame.K_DOWN] or key[pygame.K_s]:
                self.hop((0, 1))
            elif key[pygame.K_F2]:
                config.debug_mode = not config.debug_mode
            elif key[pygame.K_F3] and config.debug_mode:
                print("goals met %s" % self.goals_reached)

    def got_all_goals(self):
        """return true iff there is at least one empty goal"""
        rows = self.current_level()
        for y in range(len(rows)):
            for x in range(len(rows[y])):
                block = rows[y][x]
                if block.terrain is Terrain.GOAL and (x, y) not in self.goals_reached:
                    # found an unmet goal, bail out
                    return False
        # no unmet goal found
        return True

    def hop(self, j):
        """jump the frog by the given block vector j, except if the frog is blocked"""
        new_x = self.frog_pos[X] + j[X]
        new_y = self.frog_pos[Y] + j[Y]
        if config.debug_mode and self.riding is not None:
            print("riding at %s,%s hopping to %s,%s" % (self.frog_pos[X], self.frog_pos[Y], new_x, new_y))

        rows = self.current_level()
        if 0 <= new_y < len(rows) and 0 <= new_x < len(rows[new_y]):
            block = rows[math.floor(new_y)][math.floor(new_x)]
            # now check the block to see if it is passable
            new_pos = (new_x, new_y)
            if block.is_passable() and new_pos not in self.goals_reached:
                self.frog_pos = new_pos
                if block.terrain is Terrain.GOAL:
                    self.goal(new_pos)
                elif block.terrain is Terrain.FATAL and not self.rideable_at(new_pos):
                    self.die()
                else:
                    # post-hop if frog is on a rideable vehicle, store that and frog offset from it
                    colliding = list(filter(lambda v: v.collides_with(new_pos), self.vehicles))
                    if len(colliding) > 0:
                        self.riding = list(colliding)[0]  # Highlander mode - there can be only one
                        self.riding_x_offset = new_x - self.riding.pos[X]
                    else:
                        self.riding = None
        elif config.debug_mode:
            print("frog move prohibited: %s + %s" % (self.frog_pos, j,))
        self.obey_controls_at = pygame.time.get_ticks() + 100

    def goal(self, pos):
        """Record achievement of the goal at pos"""
        corrected_pos = (round(pos[X]), round(pos[Y]))  # jumping from vehicle gives fractional pos
        self.goals_reached.append(corrected_pos)
        self.score += 10
        self.game_state = LEVEL_COMPLETE
        self.play_at = pygame.time.get_ticks() + 1000
        self.reset_frog()

    def next_level(self):
        """proceed to the next game level"""
        self.level_num = (self.level_num + 1) % len(config.levels)
        self.recalculate_sizes(self.current_level())
        self.start_level()

    def die(self):
        """This froggy's gone to heaven..."""
        self.lives = self.lives - 1
        if config.debug_mode:
            print("died at %s; %s" % (self.frog_pos, self.vehicles))
        if self.lives <= 0:
            self.frog_pos = (-1, -1)  # move him off the screen
            self.game_state = GAME_OVER
            self.title_at = pygame.time.get_ticks() + 3000
        else:
            self.reset_frog()
            self.get_ready()

    def rideable_at(self, pos):
        """Returns true iff the given position is currently occupied by a rideable vehicle"""
        return list(filter(lambda v: v.rideable and v.collides_with(pos), self.vehicles))

    def is_on_screen(self, pos):
        """Returns true iff the given position is within the playable game area."""
        corrected_pos = (round(pos[X]), round(pos[Y]))
        rows = self.current_level()
        return 0 <= corrected_pos[Y] < len(rows) and 0 <= corrected_pos[X] < len(rows[corrected_pos[Y]])

    def recalculate_sizes(self, rows):
        """Dynamically scale the size and layout of text, playfield etc., preserving
        the aspect ratio and margins. Note that this is initialisation called from
        the constructor (which is a bit naughty) but also on window resize and level up"""

        # calculate playfield size in blocks
        # find the widest row
        self.playfield_wb = max(map(lambda x: len(x), rows))
        self.playfield_hb = len(rows)
        if config.debug_mode:
            print("widest row=%s" % self.playfield_wb)

        # calculate font sizes
        screen_h = self.screen.get_height()
        self.shortest = min(self.screen.get_width(), screen_h)
        self.big_font_size = round(self.shortest * config.font_scale / 10)
        self.little_font_size = round(self.big_font_size * config.font_scale * 0.4)
        self.big_font = pygame.font.Font(config.font_name, self.big_font_size)
        self.little_font = pygame.font.Font(config.font_name, self.little_font_size)
        self.debug_font = pygame.font.Font(pygame.font.get_default_font(), 12)

        # status is at the bottom of the screen
        self.status_top = screen_h - self.little_font.get_height() * 1.4
        # scoreboard is at the top
        self.scoreboard_top = round(self.little_font.get_height() * 0.5)
        # playfield goes under scoreboard, which during gameplay is little_font
        self.playfield_top = round(self.scoreboard_top + self.little_font.get_height() * 1.2)
        # figure out the size of square blocks that fit the playfield
        playfield_height = self.status_top - self.playfield_top
        f = math.floor
        block_width = f(self.screen.get_width() / self.playfield_wb)
        block_height = f(playfield_height / self.playfield_hb)
        self.block_size = min(block_height, block_width)
        self.block = (self.block_size, self.block_size)
        self.game_width = self.block_size * self.playfield_wb
        self.game_height = self.block_size * self.playfield_hb
        # centre horizontally and vertically
        self.game_x = f((self.screen.get_width() - self.game_width) / 2)
        self.game_y = f((self.status_top - self.game_height + self.playfield_top) / 2)

    def current_level(self):
        return config.levels[self.level_num]["level"]

    def pos_to_pixels(self, pos):
        """returns a tuple of pixel coordinates for the given block other"""
        px = pos[X] * self.block_size + self.game_x
        py = pos[Y] * self.block_size + self.game_y
        return px, py

    def playfield_clip(self):
        """returns a rectangle within which game drawing may occur"""
        return Rect(self.game_x, self.game_y, self.game_width, self.game_height)

    def draw(self):
        """main routine to draw whole frame"""
        state = self.game_state
        if state == TITLE:
            self.draw_title()
        elif state in (PLAYING, GET_READY, GAME_OVER, LEVEL_COMPLETE):
            self.draw_playfield()
            if state == GET_READY:
                self.draw_flashing_text("Level %s Get Ready!" % self.level_num)
            elif state == GAME_OVER:
                self.draw_flashing_text("Game Over")
            elif state == LEVEL_COMPLETE:
                self.draw_flashing_text("Level Complete")

    def draw_fancy_text(self, font, text, y):
        """draw centred text in font with fancy effect at screen height y"""
        stack = ((6, config.title_shadow), (4, config.title_fg), (2, config.title_shadow), (0, config.title_fg))
        for tt in stack:
            t = font.render(text, True, tt[1])
            text_rect = t.get_rect()
            text_rect.x = self.screen.get_width() / 2 - text_rect.width / 2 + tt[0]
            text_rect.y = y + tt[0]
            self.screen.blit(t, text_rect)

    def draw_flashing_text(self, mesg):
        if (round(pygame.time.get_ticks() / 200)) % 3 > 0:
            self.draw_fancy_text(self.little_font, mesg, self.screen.get_height() / 2)

    def draw_goals_reached(self):
        """draw goals reached"""
        for g in self.goals_reached:
            x, y = self.pos_to_pixels(g)
            shrink = self.block_size / -2  # half-sized
            rect = Rect(x, y, self.block_size, self.block_size).inflate(shrink, shrink)
            pygame.draw.rect(self.screen, config.frog_colour, rect)

    def draw_level(self):
        """draw the actual game area from the current level config"""
        level = self.current_level()
        for y in range(len(level)):
            row = level[y]
            for x in range(len(row)):
                block = row[x]
                px, py = self.pos_to_pixels((x, y))
                rect = Rect(px, py, self.block_size, self.block_size)
                block.draw(self.screen, rect)

    def draw_playfield(self):
        """draw game play screen including scoreboard and status bar"""
        self.screen.fill(config.border)
        self.draw_scoreboard(self.scoreboard_top)
        self.draw_level()
        self.draw_goals_reached()
        self.draw_sprites()
        self.draw_status()
        if config.debug_mode:
            self.draw_debug()

    def draw_scoreboard(self, y):
        scoreboard = 'SCORE %d  HIGH SCORE %d' % (self.score, self.high_score)
        self.draw_fancy_text(self.little_font, scoreboard, y)

    def draw_sprites(self):
        # draw vehicles
        for v in self.vehicles:
            v.draw(self.screen, lambda pos: self.pos_to_pixels(pos), self.block_size, self.playfield_clip())

        # draw player
        inset = self.block_size * -0.4

        frog_rect = Rect(self.pos_to_pixels(self.frog_pos), self.block)
        frog = frog_rect.inflate(inset, inset).clip(self.playfield_clip())
        pygame.draw.rect(self.screen, config.frog_colour, frog)
        if config.debug_mode:
            self.draw_debug_text("%s,%s" % (frog_rect.x, frog_rect.y), frog_rect.x, frog_rect.y)

    def draw_status(self):
        time_left = max(0, math.ceil((self.timer - pygame.time.get_ticks()) / 1000))
        text = "lives: %s    time: %d" % (self.lives, time_left)
        self.draw_fancy_text(self.little_font, text, self.screen.get_height() - self.little_font_size * 1.3)

    def draw_title(self):
        self.screen.fill(config.background)
        self.draw_fancy_text(self.big_font, config.game_name, self.big_font_size / 2)
        version_string = "v %s" % VERSION
        height = self.screen.get_height()
        self.draw_fancy_text(self.little_font, version_string, height / 3.9)
        self.draw_fancy_text(self.little_font, config.byline, height / 2.5)
        self.draw_flashing_text(config.instructions)
        self.draw_scoreboard(round(height - self.little_font.get_height() * 1.5))

    def draw_debug(self):
        """draws a lot of stuff on the screen to show key lines and where the blocks are
        just to help find problems with layout"""
        scoreboard_bottom = self.scoreboard_top + self.little_font.get_height()
        s = self.screen
        sw = s.get_width()
        sh = s.get_height()
        # game_area = Rect(self.game_x, self.game_y, self.game_width, self.game_height)
        # pygame.draw.rect(s, config.light_grey, game_area)
        for row in range(self.playfield_hb):
            for block in range(self.playfield_wb):
                sx = block * self.block_size + 2 + self.game_x
                sy = row * self.block_size + 2 + self.game_y
                inset_width = self.block_size - 4
                tl = (sx + 4, sy + 4)
                tr = (sx + 4, sy + inset_width)
                bl = (sx + 4, sy + inset_width)
                br = (sx + inset_width, sy + inset_width)
                pygame.draw.line(s, config.black, tl, tr)
                pygame.draw.line(s, config.black, tr, br)
                pygame.draw.line(s, config.black, br, bl)
                pygame.draw.line(s, config.black, bl, tl)
                self.draw_debug_text("%s,%s" % (sx, sy), sx, sy)
                pygame.draw.line(self.screen, config.yellow, (sx, sy), (sx + 10, sy - 10))

        def ln(colour, y):
            pygame.draw.line(s, colour, (0, y), (sw, y))

        # some horizontal lines to check layout
        ln(config.blue, self.scoreboard_top)
        ln(config.blue, scoreboard_bottom)
        ln(config.white, self.playfield_top)
        ln(config.purple, self.game_y)
        ln(config.orange, self.status_top)
        gdy = self.game_y - self.playfield_top
        params = (self.playfield_wb, self.playfield_hb, self.block_size, sw, sh, gdy)
        dbg_txt = "blocks %sx%s @ %spx %sx%s | gdy: %s" % params
        self.draw_debug_text(dbg_txt, 10, sh)

    def draw_debug_text(self, dbg_txt, x, y):
        t = self.debug_font.render(dbg_txt, True, config.white, config.dark_grey)
        text_rect = t.get_rect()
        text_rect.x = x
        text_rect.y = y - text_rect.height - 10
        self.screen.blit(t, text_rect)


if __name__ == '__main__':
    Game().loop()
    sys.exit(0)
