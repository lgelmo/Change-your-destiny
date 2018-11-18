import pygame as py
import sys
#import mathutils
import math
import time
import random
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm

# PRZYDATNE FUNKCJE

def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z
def length(v):
    x,y,z = v
    return math.sqrt(x*x + y*y + z*z)
def vector(b,e):
    x,y,z = b
    X,Y,Z = e
    return (X-x, Y-y, Z-z)
def unit(v):
    x,y,z = v
    mag = length(v)
    return (x/mag, y/mag, z/mag)
def distance(p0,p1):
    return length(vector(p0,p1))
def scale(v,sc):
    x,y,z = v
    return (x * sc, y * sc, z * sc)
def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)
def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist)

def dist(pt1,pt2):
    return ( ((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**(1/2) )

def dist_to_line(pt,l_pkt1,l_pkt2):

    dist=pnt2line((pt[0],pt[1],0),(l_pkt1[0],l_pkt1[1],0),(l_pkt2[0],l_pkt2[1],0))
    return(dist)
    #x=mathutils.geometry.intersect_point_line(pt,l_pkt1,l_pkt2)
    # y=(x[0][0],x[0][1])
    # if x[1]<0:
    #     return(dist(pt,l_pkt1))
    # elif x[1]<1:
    #     return (dist(pt, y))
    # else:
    #     return (dist(pt, l_pkt2))


max_tps = 700.0

#Zmienne globalne
rect_rozmiar = 50
trawa_wysokosc = 40

jump_size = 100
jump_count = 0

jump_active = False

FIRE_IN_THE_HOLE = False
BUM=False
BUM2=False


dl_celownika=80
shoot_time=0
max_shoot_speed=180

gravity=3.5
max_turn_time=10
menu_pos=4
set_pos=3

pause_time=0
pause_start_time=0

exp_min_x = -1000
exp_min_y = -1000

map1_ind=1
map2_ind=2
map3_ind=3
map4_ind=4
map5_ind=5

mapping_pos=5
#########################################################################################

py.init()

#Teksty
myfont = py.font.SysFont("monospace", 20)
text1 = myfont.render("Test your might!", 1, (255,255,0))

font_duzy = py.font.SysFont("monospace", 40)

l00=font_duzy.render("0", 1, (255,255,0))
l01=font_duzy.render("1", 1, (255,255,0))
l02=font_duzy.render("2", 1, (255,255,0))
l03=font_duzy.render("3", 1, (255,255,0))
l04=font_duzy.render("4", 1, (255,255,0))
l05=font_duzy.render("5", 1, (255,255,0))
l06=font_duzy.render("6", 1, (255,255,0))
l07=font_duzy.render("7", 1, (255,255,0))
l08=font_duzy.render("8", 1, (255,255,0))
l09=font_duzy.render("9", 1, (255,255,0))
l10=font_duzy.render("10", 1, (255,255,0))
l11=font_duzy.render("11", 1, (255,255,0))
l12=font_duzy.render("12", 1, (255,255,0))
l13=font_duzy.render("13", 1, (255,255,0))
l14=font_duzy.render("14", 1, (255,255,0))
l15=font_duzy.render("15", 1, (255,255,0))
l16=font_duzy.render("16", 1, (255,255,0))
l17=font_duzy.render("17", 1, (255,255,0))
l18=font_duzy.render("18", 1, (255,255,0))
l19=font_duzy.render("19", 1, (255,255,0))
l20=font_duzy.render("20", 1, (255,255,0))

lzero=font_duzy.render("0", 1, (128, 128, 128))

liczby=[l00,l01,l02,l03,l04,l05,l06,l07,l08,l09,l10,
        l11, l12, l13, l14, l15, l16, l17, l18, l19, l20]

font2 = py.font.SysFont("monospace", 30)
score_0_0=font2.render("0/0", 1, (255,255,0))
score_1_0=font2.render("1/0", 1, (255,255,0))
score_0_1=font2.render("0/1", 1, (255,255,0))
score_1_1=font2.render("1/1", 1, (255,255,0))
score_2_1=font2.render("2/1", 1, (255,255,0))
score_1_2=font2.render("1/2", 1, (255,255,0))
score_2_2=font2.render("2/2", 1, (255,255,0))
score_2_0=font2.render("2/0", 1, (255,255,0))
score_0_2=font2.render("0/2", 1, (255,255,0))

## Pozycje startowe

red_body_radius=20
red_left=False
red_shoot_mode=False
red_shoot_start=False
red_shoot_angle=0
red_shoot_v0=0
red_HP=100
trafienie_red=False
red_turn_time=7
red_score=0
red_PEW=False
red_shots=1

blue_body_radius=20
blue_left=True
blue_shoot_mode=False
blue_shoot_start=False
blue_shoot_angle=0
blue_shoot_v0=0
blue_HP=100
trafienie_blue=False
blue_turn_time=0
blue_score=0
blue_PEW=False
blue_shots=1

red_turn=True
First_turn=True

## Dane Broni
shot_start_x=0
shot_start_y=0
shot_angle=0
#bazooka
ammo_r=10

#Explozja i dmg
exp_x=-100
exp_y=-100
exp_ani=0

dmg_x = -100
dmg_y = -100

dm_x = -100
dm_y = -100

ammo_x=-200
ammo_y=-200

idzie_lewo=False
idzie_prawo=False
####################

def rocket_dmg(x):
    return(30*((3*blue_body_radius-x)/(2*blue_body_radius-ammo_r))+10)

####################
#####  GRAFIKI  ####

kot_l = py.image.load("Grafika/cat_l.png")
kot_l = py.transform.scale(kot_l, (40, 40))

kot_p = py.image.load("Grafika/cat_r.png")
kot_p = py.transform.scale(kot_p, (40, 40))

pies_l = py.image.load("Grafika/pies_l.png")
pies_l = py.transform.scale(pies_l, (40, 40))

pies_p = py.image.load("Grafika/pies_r.png")
pies_p = py.transform.scale(pies_p, (40, 40))

#Explozje
expl_1 = py.image.load("Grafika/expl_1.png")
expl_2 = py.image.load("Grafika/expl_2.png")
expl_3 = py.image.load("Grafika/expl_3.png")
expl_4 = py.image.load("Grafika/expl_4.png")
expl_5 = py.image.load("Grafika/expl_5.png")
expl_6 = py.image.load("Grafika/expl_6.png")
expl_7 = py.image.load("Grafika/expl_7.png")
expl_8 = py.image.load("Grafika/expl_8.png")
expl_9 = py.image.load("Grafika/expl_9.png")
expl_10 = py.image.load("Grafika/expl_10.png")
expl_11 = py.image.load("Grafika/expl_11.png")
expl_12 = py.image.load("Grafika/expl_12.png")

Exp=[expl_1,expl_2,expl_3,expl_4,expl_5,expl_6,expl_7,expl_8,expl_9,expl_10,expl_11,expl_12]

def cat_l(x,y):
    screen.blit(kot_l, (x, y))
def cat_p(x, y):
    screen.blit(kot_p, (x, y))
def doge_l(x,y):
    screen.blit(pies_l, (x, y))
def doge_p(x,y):
    screen.blit(pies_p, (x, y))

kot_win = py.image.load("Grafika/kotel.jpg")
pies_win = py.image.load("Grafika/piesel.jpg")

tlo1 = py.image.load(("Grafika/tlo1.jpg"))

########################
######  DZWIEKI  #######
py.mixer.init()
#py.mixer.music.load('DzwiekMortal Kombat.mp3')
#py.mixer.music.play(-1)

#muza = py.mixer.Sound('Mortal Kombat.mp3')

wof = py.mixer.Sound('Dzwiek/bark.wav')
miow = py.mixer.Sound('Dzwiek/cat_w.wav')
muza = py.mixer.Sound('Dzwiek/Mortal Kombat.wav')

#py.mixer.Channel(0).play(wof)
#py.mixer.Channel(1).play(miow)

py.mixer.Channel(2).play(muza)
py.mixer.music.set_volume(0)

vol=py.mixer.music.get_volume()
volu=py.mixer.music.get_volume()

########################
teren1=[
    (0,680,1280,680), #jakaś linia
    (0,0,0,719), #lewa ściana
    (1280,0,1280,720), #prawa sciana
    # (0,0,1280,0), #sufit

    (0,680-160,160,680), # dolny lewy tr
    (1280,680-160,1280-160,680,), # dolny prawy tr

    (6*32,680-6*28,11*32,680-6*28), # dolny lewy wyzszy tr
    (6*32,680-6*28,11*32,680-6*28-4*28),
    (11*32,680-6*28-4*28,11*32,680-6*28),

    (1280-6*32,680-6*28,1280-11*32,680-6*28), #dolny prawy wyzszy tr
    (1280-6 * 32, 680 - 6 * 28, 1280-11 * 32, 680 - 6 * 28 - 4 * 28),
    (1280-11 * 32, 680 - 6 * 28 - 4 * 28, 1280-11 * 32, 680 - 6 * 28),

    (11*32,680,14*32,680-2*28), # dolne torjkaty 1
    (14*32,680-2*28,17*32,680),
    (1280-11 * 32, 680, 1280-14 * 32, 680 - 2 * 28), # dolne torjkaty 2
    (1280-14 * 32, 680 - 2 * 28, 1280-17 * 32, 680),

    (14 * 32, 680-7*28, 16 * 32,680-7*28), # kreseczki dolne
    (18 * 32, 680-7*28, 19 * 32,680-7*28),
    (21 * 32, 680-7*28, 22 * 32,680-7*28),
    (24 * 32, 680-7*28, 26 * 32,680-7*28),

    # schodki
    (6*32,680-10*28,7*32,680-10*28), # najblizsze trójkąta
    (1280-6*32,680-10*28,1280-7*32,680-10*28),

    (2* 32, 680 - 11 * 28, 3 * 32, 680 - 11 * 28), # nastepne
    (1280 - 2 * 32, 680 - 11 * 28, 1280 - 3 * 32, 680 - 11 * 28),

    (0, 680 - 13 * 28, 1*32, 680 - 13 * 28),  # nastepne
    (1280, 680 - 13 * 28, 1280-1*32, 680 - 13 * 28),

    (2* 32, 680 - 15 * 28, 3 * 32, 680 - 15 * 28), # nastepne
    (1280 - 2 * 32, 680 - 15 * 28, 1280 - 3 * 32, 680 - 15 * 28),

    (5*32,9*28,10*32,4*28), # gorna tarka lewa
    (6*32,8*28,7*32,8*28),
    (7*32,8*28,7*32,7*28),
    (7*32,7*28,8*32,7*28),
    (8*32,7*28,8*32,6*28),
    (8*32,6*28,9*32,6*28),
    (9*32,6*28,9*32,5*28),

    (1280-5 * 32, 9 * 28, 1280-10 * 32, 4 * 28),  # gorna tarka prawa
    (1280-6 * 32, 8 * 28, 1280-7 * 32, 8 * 28),
    (1280-7 * 32, 8 * 28, 1280-7 * 32, 7 * 28),
    (1280-7 * 32, 7 * 28, 1280-8 * 32, 7 * 28),
    (1280-8 * 32, 7 * 28, 1280-8 * 32, 6 * 28),
    (1280-8 * 32, 6 * 28, 1280-9 * 32, 6 * 28),
    (1280-9 * 32, 6 * 28, 1280-9 * 32, 5 * 28),

    (13*32,3*28,15*32,3*28),
    (19*32,3*28,21*32,3*28),
    (25*32,3*28,27*32,3*28),
]
t1_red_start_x=32
t1_red_start_y=680-12*28
t1_blue_start_x=1280-30
t1_blue_start_y=680-12*28
miny1=[[32*14,680-100],[1280-32*14,680-100],[18*32+16,680-300],[21*32+16,680-300]]

teren2=[

    #(0, 680, 1280, 680),  # jakaś linia
    (0, 0, 0, 719),  # lewa ściana
    (1280, 0, 1280, 720),  # prawa sciana

    (2*32,680-5*28,3*32,680-5*28), #lewe schody
    (0*32,680-8*28,1*32,680-8*28),
    (2*32,680-11*28,3*32,680-11*28),
    (0*32,680-14*28,1*32,680-14*28),
    (5*32,680-13*28,6*32,680-13*28),

    (4*32,680-16*28,2*32,680-17*28), # red zamek
    (3*32,680-19*28,5*32,680-20*28),
    (6*32,680-17*28,8*32,680-18*28),
    (8*32,680-21*28,10*32,680-20*28),

    (4*32,680-3*28,9*32,680-3*28), # dolne kladki
    (13*32,680-2*28,18*32,680-2*28),
    (22*32,680-1*28,27*32,680-1*28),

    (12*32,680-21*28,17*32,680-21*28), # gorne klaski
    (21 * 32, 680 - 20 * 28, 26 * 32, 680 - 20 * 28),
    (30 * 32, 680 - 19 * 28, 35 * 32, 680 - 19 * 28),

    (29 * 32, 680 - 3 * 28, 31 * 32, 680 - 2 * 28), # blue zamek
    (30 * 32, 680 - 5 * 28, 32 * 32, 680 - 6 * 28),
    (33 * 32, 680 - 3 * 28, 35 * 32, 680 - 4 * 28),
    (35 * 32, 680 - 7 * 28, 37 * 32, 680 - 6 * 28),

    (36 * 32, 680 - 16 * 28, 37 * 32, 680 - 16 * 28), # lewe schody
    (1280-0*32,680-8*28,1280-1*32,680-8*28),
    (1280-2*32,680-11*28,1280-3*32,680-11*28),
    (1280-0*32,680-14*28,1280-1*32,680-14*28),
    (1280-1*32,680-18*28,1280-2*32,680-18*28),

    (640-40,340,640,340-40),
    (640,340-40,640+40,340),
    (640+40,340,640,340+40),
    (640,340+40,640-40,340),
]
t2_red_start_x=3*32
t2_red_start_y=0
t2_blue_start_x=1280-7*32
t2_blue_start_y=720-200
miny2=[[6*32+16,500],[15*32+16,500],[24*32+16,500],
       [14 * 32 + 16, 50], [23 * 32 + 16, 100], [32 * 32 + 16, 100]]

teren3=[

(0, 680, 1280, 680),  # jakaś linia
(0, 0, 0, 719),  # lewa ściana
(1280, 0, 1280, 720),  # prawa sciana

(0,680-2*35,3*32,680-2*35),     # pierwsze liie od dolu
(6*32,680-2*35,22*32,680-2*35),
(24*32,680-2*35,34*32,680-2*35),
(36*32,680-2*35,40*32,680-2*35),

(2*32,680-4*35,10*32,680-4*35),
(12*32,680-4*35,22*32,680-4*35),
(24*32,680-4*35,37*32,680-4*35),

(0*32,680-6*35,5*32,680-6*35),
(7*32,680-6*35,21*32,680-6*35),
(25*32,680-6*35,34*32,680-6*35),
(36*32,680-6*35,40*32,680-6*35),

(2*32,680-8*35,12*32,680-8*35),
(14*32,680-8*35,21*32,680-8*35),
(25*32,680-8*35,28*32,680-8*35),
(30*32,680-8*35,37*32,680-8*35),

(0*32,680-10*35,2*32,680-10*35),
(4*32,680-10*35,8*32,680-10*35),
(10*32,680-10*35,22*32,680-10*35),
(24*32,680-10*35,34*32,680-10*35),
(36*32,680-10*35,40*32,680-10*35),

(0*32,680-12*35,5*32,680-12*35),
(7*32,680-12*35,17*32,680-12*35),
(29*32,680-12*35,36*32,680-12*35),

(5*32,680-14*35,11*32,680-14*35),
(13*32,680-14*35,19*32,680-14*35),
(27*32,680-14*35,34*32,680-14*35),

(0*32,680-16*35,5*32,680-16*35),
(19*32,680-16*35,22*32,680-16*35),
(24*32,680-16*35,27*32,680-16*35),
(36*32,680-16*35,40*32,680-16*35),

(5*32,680-16*35,5*32,680-12*35), #pionowe
(19*32,680-16*35,19*32,680-10*35),
(22*32,680-16*35,22*32,680-10*35),
(24*32,680-16*35,24*32,680-10*35),
(27*32,680-16*35,27*32,680-10*35),
(36*32,680-16*35,36*32,680-10*35),

(21*32,680-8*35,21*32,680-6*35),
(25*32,680-8*35,25*32,680-6*35),
]
t3_red_start_x=round(1.5*32)
t3_red_start_y=680-3*35
t3_blue_start_x=1280-6*32
t3_blue_start_y=680-13*35
miny3=[]

teren4=[
#(0, 680, 1280, 680),
(0, 0, 1280, 0),  # jakaś linia
(0, 0, 0, 719),  # lewa ściana
(1280, 0, 1280, 720),  # prawa sciana

(640-2*32,680-0*28,640-0*32,680-6*28), # trojkaty srodkowe
(640+2*32,680-0*28,640-0*32,680-6*28),
(640-2*32,0*28,640-0*32,6*28),
(640+2*32,0*28,640-0*32,6*28),

(640 - 40, 340, 640, 340 - 40), #srodek
(640, 340 - 40, 640 + 40, 340),
(640 + 40, 340, 640, 340 + 40),
(640, 340 + 40, 640 - 40, 340),

(0,680-4*28,2*32,680-4*28), ## lewe
(0,680-7*28,1*32,680-7*28),
(0,680-10*28,1*32,680-10*28),
(0,680-13*28,1*32,680-13*28),
(0,680-16*28,1*32,680-16*28),
(0,680-19*28,1*32,680-19*28),

(4*32,680-19*28,5*32,680-19*28),
(5*32,680-19*28,6*32,680-18*28),

(5*32,680-4*28,7*32,680-4*28),
(7*32,680-4*28,8*32,680-6*28),


(1280-0,680-4*28,1280-2*32,680-4*28), ## prawe
(1280-0,680-7*28,1280-1*32,680-7*28),
(1280-0,680-10*28,1280-1*32,680-10*28),
(1280-0,680-13*28,1280-1*32,680-13*28),
(1280-0,680-16*28,1280-1*32,680-16*28),
(1280-0,680-19*28,1280-1*32,680-19*28),

(1280-4*32,680-19*28,1280-5*32,680-19*28),
(1280-5*32,680-19*28,1280-6*32,680-18*28),

(1280-5*32,680-4*28,1280-7*32,680-4*28),
(1280-7*32,680-4*28,1280-8*32,680-6*28),

]
t4_red_start_x=6*32
t4_red_start_y=680-13*35
t4_blue_start_x=1280-6*32
t4_blue_start_y=680-13*35
miny4=[[19*32,680-500],[1280-19*32,680-500],[18*32+16,680-300],[21*32+16,680-300],[20*32,680-500],[20*32,680-250] ]

teren5=[
(0, 680, 1280, 680),  # jakaś linia
(0, 0, 0, 719),  # lewa ściana
(1280, 0, 1280, 720),  # prawa sciana

(0,680-4*28,4*32,680),    # dolne trojk
(1280-0,680-4*28,1280-4*32,680),

(3*32,680-5*28,5*32,680-5*28), # dolne strukt
(10*32,680-4*28,14*32,680-4*28),
(10*32,680-4*28,12*32,680-6*28),
(12*32,680-6*28,14*32,680-4*28),
(640-1*32,680-0*32,640,680-3*28),

(1280-3*32,680-5*28,1280-5*32,680-5*28), # dolne strukt
(1280-10*32,680-4*28,1280-14*32,680-4*28),
(1280-10*32,680-4*28,1280-12*32,680-6*28),
(1280-12*32,680-6*28,1280-14*32,680-4*28),
(1280-640+1*32,680-0*32,1280-640,680-3*28),

(12*32,680-12*28,1280-12*32,680-12*28), # nizsza tarka
(11*32,680-13*28,13*32,680-11*28),
(12*32,680-12*28,13*32,680-11*28),
(14*32,680-12*28,15*32,680-11*28),
(16*32,680-12*28,17*32,680-11*28),
(18*32,680-12*28,19*32,680-11*28),
(20*32,680-12*28,21*32,680-11*28),
(22*32,680-12*28,23*32,680-11*28),
(24*32,680-12*28,25*32,680-11*28),
(26*32,680-12*28,27*32,680-11*28),
(1280-11*32,680-13*28,1280-13*32,680-11*28),
(1280-12*32,680-12*28,1280-13*32,680-11*28),
(1280-14*32,680-12*28,1280-15*32,680-11*28),
(1280-16*32,680-12*28,1280-17*32,680-11*28),
(1280-18*32,680-12*28,1280-19*32,680-11*28),
(1280-20*32,680-12*28,1280-21*32,680-11*28),
(1280-22*32,680-12*28,1280-23*32,680-11*28),
(1280-24*32,680-12*28,1280-25*32,680-11*28),
(1280-26*32,680-12*28,1280-27*32,680-11*28),

(13*32,680-21*28,1280-13*32,680-21*28), #wyzsza tarka
(13*32,680-21*28,14*32,680-20*28),
(15*32,680-21*28,16*32,680-20*28),
(17*32,680-21*28,18*32,680-20*28),
(19*32,680-21*28,20*32,680-20*28),
(21*32,680-21*28,22*32,680-20*28),
(23*32,680-21*28,24*32,680-20*28),
(25*32,680-21*28,26*32,680-20*28),
(1280-13*32,680-21*28,1280-14*32,680-20*28),
(1280-15*32,680-21*28,1280-16*32,680-20*28),
(1280-17*32,680-21*28,1280-18*32,680-20*28),
(1280-19*32,680-21*28,1280-20*32,680-20*28),
(1280-21*32,680-21*28,1280-22*32,680-20*28),
(1280-23*32,680-21*28,1280-24*32,680-20*28),
(1280-25*32,680-21*28,1280-26*32,680-20*28),

(0,680-13*28,4*32,680-17*28),   #lewy monolit
(4*32,680-17*28,0,680-21*28),

(1280-0,680-13*28,1280-4*32,680-17*28),  # prawy moonolit
(1280-4*32,680-17*28,1280-0,680-21*28),

(7*32,680-8*28,8*32,680-8*28),
(10*32,680-11*28,11*32,680-11*28),

(1280-7*32,680-8*28,1280-8*32,680-8*28),
(1280-10*32,680-11*28,1280-11*32,680-11*28),

(6*32,680-15*28,7*32,680-15*28),
(1280-6*32,680-15*28,1280-7*32,680-15*28),

(4*32,680-22*28,5*32,680-22*28),
(8*32,680-21*28,9*32,680-21*28),

(1280-4*32,680-22*28,1280-5*32,680-22*28),
(1280-8*32,680-21*28,1280-9*32,680-21*28),

]
t5_red_start_x=32
t5_red_start_y=680-5*35
t5_blue_start_x=1280-32
t5_blue_start_y=680-5*35
miny5=[[12*32,680-6*28-20],[1280-12*32,680-6*28-20],[640,500],[640-32,200],[640+32,200]]

tereny=[teren1,teren2,teren3,teren4,teren5]
ter_red_xs=[t1_red_start_x,t2_red_start_x,t3_red_start_x,t4_red_start_x,t5_red_start_x]
ter_red_ys=[t1_red_start_y,t2_red_start_y,t3_red_start_y,t4_red_start_y,t5_red_start_y]
ter_blue_xs=[t1_blue_start_x,t2_blue_start_x,t3_blue_start_x,t4_blue_start_x,t5_blue_start_x]
ter_blue_ys=[t1_blue_start_y,t2_blue_start_y,t3_blue_start_y,t4_blue_start_y,t5_blue_start_y]
pola_minowe=[miny1,miny2,miny3,miny4,miny5]

map1_graf=py.image.load('Grafika/map_the_arena.png')
map2_graf=py.image.load('Grafika/map_baba_gula_house.png')
map3_graf=py.image.load('Grafika/map_the_labyrinth.png')
map4_graf=py.image.load('Grafika/map_two_sides.png')
map5_graf=py.image.load('Grafika/map_the_jungle_world.png')

map1_graf= py.transform.scale(map1_graf, (200, 112))
map2_graf= py.transform.scale(map2_graf, (200, 112))
map3_graf= py.transform.scale(map3_graf, (200, 112))
map4_graf= py.transform.scale(map4_graf, (200, 112))
map5_graf= py.transform.scale(map5_graf, (200, 112))

def check_colision(x,y,r):
    for line in teren:
        if dist_to_line((x,y),(line[0],line[1]),(line[2],line[3]))<=r:
            return(True)
        else:
            pass
    return(False)

grass = py.Rect(0,680,1280,trawa_wysokosc)
clock = py.time.Clock()
delta=0.0

### do intra
screen1 = py.display.set_mode((600,300))
czas=0
myfont = py.font.SysFont("monospace", 20)
text1 = myfont.render("Prepare for the neverending struggle...", 1, (255,255,0))
text2 = myfont.render("the struggle between good and evil.", 1, (255,255,0))
text3 = myfont.render("Change your destiny...", 1, (255,255,0))
text4 = myfont.render("...and test your migth!", 1, (255,255,0))
text5 = myfont.render("Choose your fighter!", 1, (255,255,0))
###########
# Do menu
menu_font = py.font.SysFont("monospace", 40)
MENU_text1 =  menu_font.render("New Game", 1, (255,255,0))
MENU_text2 =  menu_font.render("Options", 1, (255,255,0))
MENU_text3 =  menu_font.render("Instruction", 1, (255,255,0))
MENU_text4 =  menu_font.render("Quit Game", 1, (255,255,0))

SET_text1 = menu_font.render("Choose Maps", 1, (255,255,0))
SET_text2 = menu_font.render("Volume", 1, (255,255,0))
SET_text3 = menu_font.render("Turn Time", 1, (255,255,0))

MAP_1 = menu_font.render("Map 1:", 1, (255,255,0))
MAP_2 = menu_font.render("Map 2:", 1, (255,255,0))
MAP_3 = menu_font.render("Map 3:", 1, (255,255,0))
MAP_4 = menu_font.render("Map 4:", 1, (255,255,0))
MAP_5= menu_font.render("Map 5:", 1, (255,255,0))
# MAPS

map_font = py.font.SysFont("monospace", 30)
m1=map_font.render("The Arena",1, (139, 0, 0))
m2=map_font.render("Sauron's Eye",1, (139, 0, 0))
m3=map_font.render("The Labyrinth",1, (139, 0, 0))
m4=map_font.render("Two sides",1, (139, 0, 0))
m5=map_font.render("Jungle World",1, (139, 0, 0))

m1y=menu_font.render("The Arena",1, (255,255,0))
m2y=menu_font.render("Sauron's Eye",1, (255,255,0))
m3y=menu_font.render("The Labyrinth",1, (255,255,0))
m4y=menu_font.render("Two sides",1, (255,255,0))
m5y=menu_font.render("Jungle World",1, (255,255,0))

maps=[m1y,m2y,m3y,m4y,m5y]

#PAUSA
PAUSE_text =  menu_font.render("PAUSED", 1, (255,255,0))

choose = py.image.load("Grafika/Choose your fighter.png")
kot = py.image.load("Grafika/Choose your fighter lewy.png")
pies = py.image.load("Grafika/Choose your fighter prawy.png")

myfont = py.font.SysFont("monospace", 20)

# WEAPONS
bazooka = py.image.load("Grafika/bazooka.png")
bazooka = py.transform.scale(bazooka, (25, 25))
snipe = py.image.load("Grafika/snipe.png")
snipe = py.transform.scale(snipe, (25, 25))

### MINY
mina_r=3
miny=miny1
def add_mine(lista_min,mina_r):

    x = random.randint(0,1280)
    y = random.randint(0,650)

    while check_colision(x,y,mina_r):
        x=random.randint(0,1280)
        y=random.randint(0,650)

    lista_min.append([x,y])
    return(lista_min)

n=0
teren = tereny[n]
red_body_x = red_body_start_x = ter_red_xs[n]
red_body_y = red_body_start_y = ter_red_ys[n]
blue_body_x = blue_body_start_x = ter_blue_xs[n]
blue_body_y = blue_body_start_y = ter_blue_ys[n]
miny=pola_minowe[n][:]

right=False
left=False

MENU = True
intro = True
PAUSE = True
BAZOOKA = True
SETTINGS=False
MAPPING=False
INSTR=False
change_vol=False
change_time=False
SWITCH=False

akt_czas = 0
old_turn_time=0

GAME_TIME=0
PAUSE_TIME=0
prev_time=0
last_switch_time=0
prev_GAME_TIME = 0
########################################################
###################  PROGRAM  ##########################
########################################################
while intro:
    czas = time.clock()
 # Obslugiwanie roznych zdarzeń
    for event in py.event.get():
        if event.type == py.QUIT:
             sys.exit(0)
        elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
             if MENU==False:
                 MENU=True
             else:
                 Menu=True
        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and czas<18:
            intro=False
        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and czas>18:
            if right or left:
                intro=False
            else:
                pass
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT:
            py.mixer.Channel(0).play(miow)
            right=False
            left=True
        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT:
            py.mixer.Channel(0).play(wof)
            right=True
            left=False

     # rysowanko
    screen1.fill((0,0,0))

    if czas<5:
        screen1.blit(text1, (50, 50))
    elif czas<10:
        screen1.blit(text2, (50, 50))
    elif czas<13:
        screen1.blit(text3, (50, 50))
    elif czas<17:
        screen1.blit(text4, (50, 50))
    elif intro:
        if czas - math.floor(czas)<0.5:
            screen1.blit(text5, (180, 15))
        if right:
            screen1.blit(pies,(0,51))
        elif left:
            screen1.blit(kot,(0,51))
        else:
            screen1.blit(choose, (0, 51))

    py.display.flip()

screen = py.display.set_mode((1280,720))
czas_start=time.clock()

while True:
 # ZDARZENIA:
 ## jednokrotne wcisniecie
    for event in py.event.get():
        # Wylaczanie za pomoca krzyrzyka
        if event.type == py.QUIT:
             sys.exit(0)
        # Menu do esc
        elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE and INSTR:
            INSTR=False
        elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE and SETTINGS and (not MAPPING) and (not INSTR):
            SETTINGS=False
        elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE and MAPPING:
            MAPPING=False
        elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                if MENU==False:
                    MENU=True
                    PAUSE=True
                    pause_start_time = time.clock()
                else:
                    MENU=False
                    PAUSE = False
                    pause_time += time.clock() - pause_start_time

        elif event.type == py.KEYDOWN and event.key == py.K_p and (not MENU):
            if PAUSE == False:
                PAUSE = True
                pause_start_time=time.clock()
            else:
                PAUSE = False
                pause_time+=time.clock()-pause_start_time
        # skakanie cz.1
        elif event.type == py.KEYDOWN and event.key == py.K_SPACE and (not PAUSE):
            if red_turn:
                if red_shoot_mode:
                    pass
                elif check_colision(red_body_x,red_body_y+1,red_body_radius):
                    jump_active = True
            else:
                if blue_shoot_mode:
                    pass
                elif check_colision(blue_body_x,blue_body_y+1,blue_body_radius):
                    jump_active = True

        # wlaczanie i wylaczenie celowania
        elif event.type == py.KEYDOWN and event.key == py.K_s and (not PAUSE):
            if red_turn and check_colision(red_body_x,red_body_y+1,red_body_radius) and red_shots==1:
                shot_start_x = red_body_x
                shot_start_y = red_body_y
                if red_shoot_mode==False:
                    red_shoot_mode=True
                else:
                    red_shoot_mode=False
                    red_shoot_angle=0
                    if red_shoot_start:
                        red_shoot_start = False
                        red_shoot_v0 = 0
            elif (not red_turn) and check_colision(blue_body_x,blue_body_y+1,blue_body_radius) and blue_shots==1:
                shot_start_x = blue_body_x
                shot_start_y = blue_body_y
                if blue_shoot_mode==False:
                    blue_shoot_mode=True
                else:
                    blue_shoot_mode=False
                    blue_shoot_angle=0
                    if blue_shoot_start:
                        blue_shoot_start = False
                        blue_shoot_v0 = 0
        # przelaczanie pomiedzy pistoletem a bazooka
        elif event.type == py.KEYDOWN and event.key == py.K_a and red_shoot_mode and (not PAUSE):
            if BAZOOKA:
                BAZOOKA=False
            else:
                BAZOOKA=True
        elif event.type == py.KEYDOWN and event.key == py.K_a and blue_shoot_mode and (not PAUSE):
            if BAZOOKA:
                BAZOOKA=False
            else:
                BAZOOKA=True
        # sila strzalu
        elif event.type == py.KEYDOWN and event.key == py.K_d and red_shoot_mode==True and (not PAUSE):
            if BAZOOKA:
                if red_shoot_start==False:
                    red_shoot_start = True
                else:
                    red_shoot_start = False
                    FIRE_IN_THE_HOLE = True
                    red_shoot_mode = False
                    shot_start_x = red_body_x
                    shot_start_y = red_body_y
                    v0 = red_shoot_v0
                    red_shoot_v0 = 0
                    shot_angle = red_shoot_angle
                    red_shoot_angle = 0
                    red_shots=0
            else:
                red_shoot_mode = False
                red_PEW=True
                shot_angle = red_shoot_angle
                red_shots = 0
        elif event.type == py.KEYDOWN and event.key == py.K_d and blue_shoot_mode==True and (not PAUSE):
            if BAZOOKA:
                if blue_shoot_start==False:
                    blue_shoot_start = True
                else:
                    blue_shoot_start = False
                    FIRE_IN_THE_HOLE = True
                    blue_shoot_mode = False
                    shot_start_x = blue_body_x
                    shot_start_y = blue_body_y
                    v0 = blue_shoot_v0
                    blue_shoot_v0 = 0
                    shot_angle = blue_shoot_angle
                    blue_shoot_angle = 0
                    blue_shots = 0
            else:
                blue_shoot_mode = False
                blue_PEW=True
                shot_angle = blue_shoot_angle
                blue_shots = 0
        # menu gora dul

        elif event.type == py.KEYDOWN and event.key == py.K_DOWN and SETTINGS and MAPPING:
            mapping_pos -= 1
            if mapping_pos< 1:
                mapping_pos = 1
        elif event.type == py.KEYDOWN and event.key == py.K_UP and SETTINGS and MAPPING:
            mapping_pos += 1
            if mapping_pos> 5:
                mapping_pos = 5

        elif event.type == py.KEYDOWN and event.key == py.K_UP and MENU and (not SETTINGS):
            menu_pos+=1
            if menu_pos>4:
                menu_pos=4
        elif event.type == py.KEYDOWN and event.key == py.K_DOWN and MENU and (not SETTINGS):
            menu_pos-=1
            if menu_pos<1:
                menu_pos=1
        elif event.type == py.KEYDOWN and event.key == py.K_UP and SETTINGS and (not change_time) and (not change_vol):
            set_pos+=1
            if set_pos>3:
                set_pos=3
        elif event.type == py.KEYDOWN and event.key == py.K_DOWN and SETTINGS and (not change_time) and (not change_vol):
            set_pos -= 1
            if set_pos < 1:
                set_pos = 1

        elif event.type == py.KEYDOWN and event.key == py.K_UP and SETTINGS and change_time:
            max_turn_time+=1
            if max_turn_time>20:
                max_turn_time=20
        elif event.type == py.KEYDOWN and event.key == py.K_DOWN and SETTINGS and change_time:
            max_turn_time -= 1
            if max_turn_time < 5:
                max_turn_time = 5

        elif event.type == py.KEYDOWN and event.key == py.K_UP and SETTINGS and change_vol:
            vol+=0.05
            if vol > 1:
                vol = 1
            py.mixer.music.set_volume(vol)
        elif event.type == py.KEYDOWN and event.key == py.K_DOWN and SETTINGS and change_vol:
            vol-=0.05
            if vol < 0:
                vol = 0
            py.mixer.music.set_volume(vol)

        # opcje w MENU

        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and MENU and SETTINGS and (set_pos==3):
            MAPPING=True
        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and MENU and menu_pos == 1:
            sys.exit(0)
        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and MENU and menu_pos == 4:
            # ladowanie nowej gry
            MENU=False
            PAUSE=False

            GAME_TIME = 0
            PAUSE_TIME = 0
            #prev_time = 0
            last_switch_time = 0
            prev_GAME_TIME = 0

            red_left = False
            red_shoot_mode = False
            red_shoot_start = False
            red_shoot_angle = 0
            red_shoot_v0 = 0
            red_HP = 100
            trafienie_red = False
            red_turn_time = 0
            red_score = 0
            red_PEW = False
            red_shots = 1

            blue_body_radius = 20
            blue_left = True
            blue_shoot_mode = False
            blue_shoot_start = False
            blue_shoot_angle = 0
            blue_shoot_v0 = 0
            blue_HP = 100
            trafienie_blue = False
            blue_turn_time = 0
            blue_PEW = False
            blue_shots = 0

            red_turn = True

            n=maps_ind[0]-1
            teren = tereny[n]
            red_body_x = red_body_start_x = ter_red_xs[n]
            red_body_y = red_body_start_y = ter_red_ys[n]
            blue_body_x = blue_body_start_x = ter_blue_xs[n]
            blue_body_y = blue_body_start_y = ter_blue_ys[n]
            miny = pola_minowe[n][:]

            #print(pola_minowe[maps_ind[0] - 1])

        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and MENU and menu_pos == 3:
            SETTINGS = True
        elif event.type == py.KEYDOWN and event.key == py.K_RETURN and MENU and menu_pos == 2:
            open("ReadMe.txt")

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and set_pos == 2 and (not MAPPING):
            change_vol = True
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and set_pos == 2 and (not MAPPING):
            change_vol = False

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and set_pos == 1 and (not MAPPING):
            change_time = True
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and set_pos == 1 and (not MAPPING):
            change_time = False

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and MAPPING and mapping_pos==5:
            map1_ind+=1
            if map1_ind>5:
                map1_ind=5
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and MAPPING and mapping_pos==5:
            map1_ind -= 1
            if map1_ind < 1:
                map1_ind = 1

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and MAPPING and mapping_pos==4:
            map2_ind+=1
            if map2_ind>5:
                map2_ind=5
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and MAPPING and mapping_pos==4:
            map2_ind -= 1
            if map2_ind < 1:
                map2_ind = 1

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and MAPPING and mapping_pos==3:
            map3_ind+=1
            if map3_ind>5:
                map3_ind=5
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and MAPPING and mapping_pos==3:
            map3_ind -= 1
            if map3_ind < 1:
                map3_ind = 1

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and MAPPING and mapping_pos==2:
            map4_ind+=1
            if map4_ind>5:
                map4_ind=5
        elif event.type == py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and MAPPING and mapping_pos==2:
            map4_ind -= 1
            if map4_ind < 1:
                map4_ind = 1

        elif event.type == py.KEYDOWN and event.key == py.K_RIGHT and SETTINGS and MAPPING and mapping_pos==1:
            map5_ind+=1
            if map5_ind>5:
                map5_ind=5
        elif event.type ==py.KEYDOWN and event.key == py.K_LEFT and SETTINGS and MAPPING and mapping_pos==1:
            map5_ind -= 1
            if map5_ind < 1:
                map5_ind = 1
##############################################################################
    # kontrola fpsow

    delta += clock.tick()/4000.0  # czas ile zajelo nam wykonianie klatki
    ### CZ OBLICZENIOWA
    while delta > 1 / max_tps:
        delta -= 1 / max_tps

    #liczenie czasu
       # GAME_TIME=time.clock()-PAUSE_TIME

    ## trzymanie klawisza
    ## Cz. obliczeniowa
        #skakanie cz.2
        if jump_active and red_turn:
            if jump_count <= jump_size:
                if check_colision(red_body_x,red_body_y-1,red_body_radius):
                    jump_count = 0
                    jump_active = False
                else:
                    red_body_y -= 1
                    jump_count += 1
            else:
                jump_count = 0
                jump_active = False
        elif jump_active and (not red_turn):
            if jump_count <= jump_size:
                if check_colision(blue_body_x,blue_body_y-1,blue_body_radius):
                    jump_count = 0
                    jump_active = False
                else:
                    blue_body_y -= 1
                    jump_count += 1
            else:
                jump_count = 0
                jump_active = False

        keys = py.key.get_pressed()

        # CONTROLA
        if keys[py.K_LEFT] and (not PAUSE):
            if red_turn:
                if red_shoot_mode:
                    pass
                elif not check_colision(red_body_x-1,red_body_y,red_body_radius):
                    red_body_x += -1
                    red_left = True
                elif not check_colision(red_body_x-1,red_body_y-1,red_body_radius):
                    red_body_x += -1
                    red_body_y += -1
                    red_left = True
                else:
                    pass
            else:
                if blue_shoot_mode:
                    pass
                elif not check_colision(blue_body_x-1,blue_body_y,blue_body_radius):
                    blue_body_x += -1
                    blue_left = True
                elif not check_colision(blue_body_x-1,blue_body_y-1,blue_body_radius):
                    blue_body_x += -1
                    blue_body_y += -1
                    blue_left = True
                else:
                    pass
        if keys[py.K_RIGHT] and (not PAUSE) :
            if red_turn:
                if red_shoot_mode:
                    pass
                elif not check_colision(red_body_x + 1, red_body_y,red_body_radius):
                    red_body_x += +1
                    red_left = False
                elif not check_colision(red_body_x + 1, red_body_y - 1,red_body_radius):
                    red_body_x += 1
                    red_body_y += -1
                    red_left = False
                else:
                    pass
            else:
                if blue_shoot_mode:
                    pass
                elif not check_colision(blue_body_x + 1, blue_body_y,blue_body_radius):
                    blue_body_x += +1
                    blue_left = False
                elif not check_colision(blue_body_x + 1, blue_body_y - 1,blue_body_radius):
                    blue_body_x += 1
                    blue_body_y += -1
                    blue_left = False
                else:
                    pass

        if keys[py.K_UP] and red_shoot_mode and (not PAUSE):
            if red_shoot_angle<90:
                red_shoot_angle+=1
            else:
                pass
        if keys[py.K_UP] and blue_shoot_mode and (not PAUSE):
            if blue_shoot_angle<90:
                blue_shoot_angle+=1
            else:
                pass
        if keys[py.K_DOWN] and red_shoot_mode and (not PAUSE):
            if red_shoot_angle>-90:
                red_shoot_angle-=1
            else:
                pass
        if keys[py.K_DOWN] and blue_shoot_mode and (not PAUSE):
             if blue_shoot_angle>-90:
                blue_shoot_angle-=1
             else:
                pass

    # samoistne spadanie
        if (not jump_active) and (not PAUSE):
            if (not check_colision(red_body_x,red_body_y+1,red_body_radius)):
                red_body_y+=1
            # elif (not check_colision(red_body_x+1,red_body_y+1)):
            #     red_body_y += 1
            #     red_body_x += 1
            # elif (not check_colision(red_body_x - 1, red_body_y + 1)):
            #     red_body_y += 1
            #     red_body_x += -1 #
        if (not jump_active) and (not PAUSE):
            if (not check_colision(blue_body_x,blue_body_y+1,blue_body_radius)):
                blue_body_y+=1
            # elif (not check_colision(red_body_x+1,red_body_y+1)):
            #     red_body_y += 1
            #     red_body_x += 1
            # elif (not check_colision(red_body_x - 1, red_body_y + 1)):
            #     red_body_y += 1
            #     red_body_x += -1

    # samoistne spadanie min
        for mina in miny:
            if (not check_colision(mina[0],mina[1],mina_r)):
                mina[1]+=1

    # rosniecie sily strzalu
        if red_shoot_start and (not PAUSE) :
            if red_shoot_v0 < max_shoot_speed:
                red_shoot_v0 += 1
            else:
                pass
        if blue_shoot_start and (not PAUSE) :
            if blue_shoot_v0 < max_shoot_speed:
                blue_shoot_v0 += 1
            else:
                pass

        ## Strzal rakieta
        # dla czerwonego gracza
        if FIRE_IN_THE_HOLE and red_turn:
            if (red_left or idzie_lewo) and (not idzie_prawo):
                idzie_lewo = True
                ammo_x = round(shot_start_x - v0 * shoot_time * math.cos(2 * math.pi * shot_angle / 360) / 30)
                ammo_y = round(shot_start_y - v0 * shoot_time * math.sin(2 * math.pi * shot_angle / 360) / 30 + (
                            1 / 2) * gravity * shoot_time ** 2 / 200)
                #py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), ammo_r)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, ammo_r):
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x, ammo_y), (blue_body_x, blue_body_y)) <= ammo_r + blue_body_radius:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= ammo_r + blue_body_radius and shoot_time > 50:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif shoot_time > 1000:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False

            elif ((not red_left) or idzie_prawo) and (not idzie_lewo):
                idzie_prawo = True
                ammo_x = round(shot_start_x + v0 * shoot_time * math.cos(2 * math.pi * shot_angle / 360) / 30)
                ammo_y = round(shot_start_y - v0 * shoot_time * math.sin(2 * math.pi * shot_angle / 360 / 30) + (
                            1 / 2) * gravity * shoot_time ** 2 / 200)
                #py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), ammo_r)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, ammo_r):
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (blue_body_x, blue_body_y)) <= ammo_r + blue_body_radius:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= ammo_r + blue_body_radius and shoot_time > 50:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif shoot_time > 1000:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
            # dla niebieskiego gracza
        if FIRE_IN_THE_HOLE and (not red_turn):
            if (blue_left or idzie_lewo) and (not idzie_prawo):
                idzie_lewo = True
                ammo_x = round(shot_start_x - v0 * shoot_time * math.cos(2 * math.pi * shot_angle / 360) / 30)
                ammo_y = round(shot_start_y - v0 * shoot_time * math.sin(2 * math.pi * shot_angle / 360) / 30 + (
                        1 / 2) * gravity * shoot_time ** 2 / 200)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, ammo_r):
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= ammo_r + red_body_radius:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x, ammo_y), (blue_body_x, blue_body_y)) <= ammo_r + blue_body_radius and shoot_time > 50:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False
                elif shoot_time > 1000:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_lewo = False

            elif ((not blue_left) or idzie_prawo) and (not idzie_lewo):
                idzie_prawo = True
                ammo_x = round(shot_start_x + v0 * shoot_time * math.cos(2 * math.pi * shot_angle / 360) / 30)
                ammo_y = round(shot_start_y - v0 * shoot_time * math.sin(2 * math.pi * shot_angle / 360 / 30) + (
                        1 / 2) * gravity * shoot_time ** 2 / 200)
               # py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), ammo_r)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, ammo_r):
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= ammo_r + red_body_radius:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= ammo_r + blue_body_radius and shoot_time > 50:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False
                elif shoot_time > 1000:
                    BUM = True
                    FIRE_IN_THE_HOLE = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dmg_x = ammo_x
                    dmg_y = ammo_y
                    idzie_prawo = False

            #### RYSOWANIE ####

        # obrazenia od rakiety
        if dist((dmg_x, dmg_y), (blue_body_x, blue_body_y)) <= blue_body_radius + ammo_r:
            py.mixer.Channel(0).play(wof)
            blue_HP -= 40
            if blue_HP < 0:
                blue_HP = 0
        elif dist((dmg_x, dmg_y), (blue_body_x, blue_body_y)) <= blue_body_radius * 3:
            py.mixer.Channel(0).play(wof)
            blue_HP -= rocket_dmg(dist((dmg_x, dmg_y), (blue_body_x, blue_body_y)))
            if blue_HP < 0:
                blue_HP = 0
        if dist((dmg_x, dmg_y), (red_body_x, red_body_y)) <= red_body_radius + ammo_r:

            py.mixer.Channel(1).play(miow)
            red_HP -= 40
            if red_HP < 0:
                red_HP = 0
        elif dist((dmg_x, dmg_y), (red_body_x, red_body_y)) <= red_body_radius * 3:
            py.mixer.Channel(0).play(miow)
            red_HP -= rocket_dmg(dist((dmg_x, dmg_y), (red_body_x, red_body_y)))
            if red_HP < 0:
                 red_HP = 0

        # niszczenie min
        el=len(miny)
        if el>0:
            i=0
            while i<el:
                if dist((dmg_x,dmg_y),(miny[i][0],miny[i][1])) <= (mina_r*10+red_body_radius):
                    exp_min_x=miny[i][0]
                    exp_min_y=miny[i][1]
                    BUM2=True
                    del miny[i]
                    i=el
                i+=1

        dmg_x = -100
        dmg_y = -100

        ## Strzal pukawka
        if red_PEW and red_turn:
            if( red_left or idzie_lewo ) and (not idzie_prawo):
                idzie_lewo=True
                ammo_x = round(shot_start_x - 4*shoot_time * math.cos(2 * math.pi * shot_angle / 360))
                ammo_y = round(shot_start_y - 4*shoot_time * math.sin(2 * math.pi * shot_angle / 360))
                #py.draw.circle(screen, (153,153,0), (ammo_x, ammo_y), 2)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y,2):
                    BUM = True
                    red_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dm_x = ammo_x
                    dm_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x,ammo_y),(blue_body_x,blue_body_y))<=2+blue_body_radius:
                    BUM = True
                    red_PEW =False
                    shoot_time =0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    py.mixer.Channel(0).play(wof)
                    blue_HP-=20
                    idzie_lewo = False
                elif shoot_time>500:
                    BUM = True
                    red_PEW =False
                    shoot_time =0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    dm_x = ammo_x
                    dm_y = ammo_y
                    idzie_lewo = False
            elif ((not red_left) or idzie_prawo ) and (not idzie_lewo):
                idzie_prawo = True
                ammo_x = round(shot_start_x + 4*shoot_time * math.cos(2 * math.pi * shot_angle / 360))
                ammo_y = round(shot_start_y - 4*shoot_time * math.sin(2 * math.pi * shot_angle / 360))
                #py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), 2)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, 2):
                    BUM = True
                    red_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (blue_body_x, blue_body_y)) <= 2 + blue_body_radius:
                    BUM = True
                    red_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    blue_HP -= 20
                    py.mixer.Channel(0).play(wof)
                    idzie_prawo = False
                elif shoot_time > 500:
                    BUM = True
                    red_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y

                    idzie_prawo = False
        if blue_PEW and (not red_turn):
            if(blue_left or idzie_lewo ) and (not idzie_prawo):
                idzie_lewo=True
                ammo_x = round(shot_start_x - 4*shoot_time * math.cos(2 * math.pi * shot_angle / 360))
                ammo_y = round(shot_start_y - 4*shoot_time * math.sin(2 * math.pi * shot_angle / 360))
                #py.draw.circle(screen, (153,153,0), (ammo_x, ammo_y), 2)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y,10):
                    BUM = True
                    blue_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_lewo = False
                elif dist((ammo_x,ammo_y),(red_body_x,red_body_y))<=2+blue_body_radius:
                    BUM = True
                    blue_PEW =False
                    shoot_time =0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_lewo = False
                    red_HP -= 20
                    py.mixer.Channel(1).play(miow)
                elif shoot_time>500:
                    BUM = True
                    blue_PEW=False
                    shoot_time =0
                    exp_x = ammo_x
                    exp_y = ammo_y

                    idzie_lewo = False
            elif ((not blue_left) or idzie_prawo ) and (not idzie_lewo):
                idzie_prawo = True
                ammo_x = round(shot_start_x + 4*shoot_time * math.cos(2 * math.pi * shot_angle / 360))
                ammo_y = round(shot_start_y - 4*shoot_time * math.sin(2 * math.pi * shot_angle / 360))
                #py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), 2)
                shoot_time += 1
                if check_colision(ammo_x, ammo_y, 2):
                    BUM = True
                    blue_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_prawo = False
                elif dist((ammo_x, ammo_y), (red_body_x, red_body_y)) <= 2 + blue_body_radius:
                    BUM = True
                    blue_PEW = False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_prawo = False
                    red_HP-=20
                    py.mixer.Channel(1).play(miow)
                elif shoot_time > 500:
                    BUM = True
                    blue_PEW= False
                    shoot_time = 0
                    exp_x = ammo_x
                    exp_y = ammo_y
                    idzie_prawo = False

        #najscie na mine
        el=len(miny)
        if el>0:
            i=0
            while i<el:
                if dist((red_body_x,red_body_y),(miny[i][0],miny[i][1])) <= (mina_r*10+red_body_radius):
                    exp_x=miny[i][0]
                    exp_y=miny[i][1]
                    BUM=True
                    red_HP-=30
                    py.mixer.Channel(1).play(miow)
                    if red_HP<0:
                        red_HP=0
                    del miny[i]
                    i=el
                i+=1
        el = len(miny)
        if el > 0:
            i = 0
            while i<el:
                if dist((blue_body_x,blue_body_y),(miny[i][0],miny[i][1])) <= (mina_r*10+red_body_radius):
                    exp_x=miny[i][0]
                    exp_y=miny[i][1]
                    BUM=True
                    blue_HP-=30
                    py.mixer.Channel(0).play(wof)
                    if blue_HP<0:
                        blue_HP=0
                    del miny[i]
                    i=el
                i+=1

        #obrazenia od utoniecia
        if red_body_y>800:
            red_HP=0
            py.mixer.Channel(1).play(miow)
        if blue_body_y>800:
            blue_HP=0
            py.mixer.Channel(0).play(wof)
        if BUM == True:  ### do POPRAWYd
            exp_ani += 0.03
            if exp_ani >= 3:
                BUM = False
                exp_ani = 0

        if BUM2 == True:  ### do POPRAWY
            exp_ani+=0.03
            if exp_ani>=3:
                BUM2 = False
                exp_ani=0

        # Czasy tury
        # if (not PAUSE):
        #     akt_czas = time.clock() - pause_time

        current_time = time.clock()
        delta_time = current_time-prev_time
        prev_time = current_time

        if PAUSE:
            PAUSE_TIME+=delta_time
        else:
            prev_GAME_TIME = GAME_TIME
            GAME_TIME+=delta_time

        turn_time=GAME_TIME % max_turn_time
        sprawdzacz=prev_GAME_TIME % max_turn_time
        if red_turn:
             #turn_time = akt_czas - czas_start
             red_turn_time = turn_time
        else:
             #turn_time = akt_czas - czas_start
             blue_turn_time = turn_time

        # zmiana tury
        if red_turn and red_turn_time<sprawdzacz and time.clock()-last_switch_time>3:
            if len(miny)<11:
                miny = add_mine(miny, mina_r)
            BAZOOKA = True
            SWITCH = True
            red_turn = False
            red_turn_time = 0
            blue_turn_time = 0
            red_shoot_mode = False
            red_shoot_start = False
            blue_shots = 1
            last_switch_time = time.clock()-PAUSE_TIME
        if (not red_turn) and blue_turn_time<sprawdzacz and time.clock()-last_switch_time>3:
            if len(miny) < 11:
                miny = add_mine(miny, mina_r)
            BAZOOKA = True
            SWITCH = True
            red_turn = True
            blue_turn_time = 0
            red_turn_time = 0
            blue_shoot_mode = False
            blue_shoot_start = False
            red_shots = 1
            last_switch_time = time.clock()-PAUSE_TIME

        # print("delta:")
        # print(delta_time)
        # print("g_time")
        # print(GAME_TIME)
        # print("prev_time")
        # print(prev_time)

        # Wygrana rundy
        if red_HP == 0 and blue_score < 2:
            red_body_x = red_body_start_x
            red_body_y = red_body_start_y
            red_left = False
            red_shoot_mode = False
            red_shoot_start = False
            red_shoot_angle = 0
            red_shoot_v0 = 0
            red_HP = 100
            trafienie_red = False
            red_turn_time = max_turn_time
            red_PEW = False
            red_shots=1

            blue_body_x = blue_body_start_x
            blue_body_y = blue_body_start_y
            blue_left = True
            blue_shoot_mode = False
            blue_shoot_start = False
            blue_shoot_angle = 0
            blue_shoot_v0 = 0
            blue_HP = 100
            trafienie_blue = False
            blue_turn_time = 0
            blue_score += 1
            blue_PEW = False
            red_turn = True
            czas_start = time.clock()
            First_turn = True
            blue_shots=0

            n=maps_ind[blue_score + red_score]-1
            teren = tereny[n]
            red_body_x = red_body_start_x = ter_red_xs[n]
            red_body_y = red_body_start_y = ter_red_ys[n]
            blue_body_x = blue_body_start_x = ter_blue_xs[n]
            blue_body_y = blue_body_start_y = ter_blue_ys[n]
            miny = pola_minowe[n][:]
        if blue_HP == 0 and red_score < 2:
            red_body_x = red_body_start_x
            red_body_y = red_body_start_y
            red_left = False
            red_shoot_mode = False
            red_shoot_start = False
            red_shoot_angle = 0
            red_shoot_v0 = 0
            red_HP = 100
            trafienie_red = False
            red_turn_time = 0
            red_score += 1
            red_PEW = False
            red_shots=0

            blue_body_x = blue_body_start_x
            blue_body_y = blue_body_start_y
            blue_body_radius = 20
            blue_left = True
            blue_shoot_mode = False
            blue_shoot_start = False
            blue_shoot_angle = 0
            blue_shoot_v0 = 0
            blue_HP = 100
            trafienie_blue = False
            blue_turn_time = max_turn_time
            blue_PEW = False
            blue_shots=1

            red_turn = False
            czas_start = time.clock()
            First_turn = True

            n=maps_ind[blue_score + red_score]-1
            teren = tereny[n]
            red_body_x = red_body_start_x = ter_red_xs[n]
            red_body_y = red_body_start_y = ter_red_ys[n]
            blue_body_x = blue_body_start_x = ter_blue_xs[n]
            blue_body_y = blue_body_start_y = ter_blue_ys[n]
            miny = pola_minowe[n][:]

        maps_ind = [map1_ind, map2_ind, map3_ind, map4_ind, map5_ind]

    ### RYSOWANIE
    if MENU and (not SETTINGS) and (not INSTR) and (not MAPPING):
        screen.fill((0,0,0))
        screen.blit(MENU_text1, (545, 200))
        screen.blit(MENU_text2, (558, 300))
        screen.blit(MENU_text3, (507, 400))
        screen.blit(MENU_text4, (535, 500))

        #py.draw.line(screen,(100,0,0),(640,0),(640,720))
        #py.draw.line(screen, (100, 0, 0), (640+100, 0), (640+100, 720))
        #py.draw.line(screen, (100, 0, 0), (640 - 100, 0), (640 - 100, 720))
        #py.Rect(0, 680, 1280, trawa_wysokosc)
        podkr=py.Rect(640-130,245+100*(-menu_pos+4),2*130,5)
        py.draw.rect(screen, (240, 230, 140), podkr)
        py.display.flip()

    if PAUSE and (not MENU):
        screen.fill((0, 0, 0))
        screen.blit(PAUSE_text, (568, 300))
        py.display.flip()

    if MENU and SETTINGS and (not MAPPING):
        screen.fill((0, 0, 0))
        screen.blit(SET_text1, (510, 250))
        screen.blit(SET_text2, (567, 350))
        screen.blit(SET_text3, (532, 450))

        screen.blit(liczby[max_turn_time],(850, 450))
        screen.blit(liczby[round(vol*20)], (850, 350))
        #py.draw.line(screen,(100,0,0),(640,0),(640,720))
        #py.draw.line(screen, (100, 0, 0), (640+100, 0), (640+100, 720))
        #py.draw.line(screen, (100, 0, 0), (640 - 100, 0), (640 - 100, 720))
        podkr1 = py.Rect(850, 295 + 100 * 2, 50, 5)
        podkr2 = py.Rect(850, 295 + 100 * 1, 50, 5)
        podkr = py.Rect(640 - 130, 295 + 100 * (-set_pos + 3), 2 * 130, 5)
        if change_time:
            py.draw.rect(screen, (240, 230, 140), podkr1)
        elif change_vol:
            py.draw.rect(screen, (240, 230, 140), podkr2)
        else:
             py.draw.rect(screen, (240, 230, 140), podkr)
        py.display.flip()

    if MAPPING:
        screen.fill((0, 0, 0))

        #nazwy pam czerwone

        screen.blit(m1, (40+20, 50+120))
        screen.blit(m2, (40+200+50-5, 50 + 120))
        screen.blit(m3, (40+2*(200+50)-15, 50 + 120))
        screen.blit(m4, (40+3*(200+50)+20, 50 + 120))
        screen.blit(m5, (40+4*(200+50)-10, 50 + 120))

        # grafiki map

        screen.blit(map1_graf, (40, 50))
        screen.blit(map2_graf, (40+200+50, 50))
        screen.blit(map3_graf, (40+2*(200+50), 50))
        screen.blit(map4_graf, (40+3*(200+50), 50))
        screen.blit(map5_graf, (40+4*(200+50), 50))

        # MAPY x:

        screen.blit(MAP_1, (400, 230))
        screen.blit(MAP_2, (400, 330))
        screen.blit(MAP_3, (400, 430))
        screen.blit(MAP_4, (400, 530))
        screen.blit(MAP_5, (400, 630))

        # nazwy map

        screen.blit(maps[map1_ind-1], (600, 230))
        screen.blit(maps[map2_ind-1], (600, 330))
        screen.blit(maps[map3_ind-1], (600, 430))
        screen.blit(maps[map4_ind-1], (600, 530))
        screen.blit(maps[map5_ind-1], (600, 630))

        # podkreslenie
        podkr = py.Rect(400, 280 + 100 * (-mapping_pos + 5), 130, 5)
        py.draw.rect(screen, (240, 230, 140), podkr)

        py.display.flip()

    #if MENU and INSTR:

    elif (not MENU) and (not PAUSE):
        screen.fill((0,0,0))
        #py.draw.rect(screen,(50,100,50),grass)
        #miny
        for mina in miny:
            py.draw.circle(screen, (155, 59, 203), (mina[0], mina[1]), mina_r)

        #Teren
        for line in teren:
            py.draw.line(screen,(50,100,50),(line[0],line[1]),(line[2],line[3]))

        py.draw.circle(screen,(185,156,140),(red_body_x,red_body_y),red_body_radius)
        py.draw.circle(screen,(194, 158, 82), (blue_body_x, blue_body_y), blue_body_radius)

        #stral rakieta
        if FIRE_IN_THE_HOLE:
            py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), ammo_r)

        if red_PEW or blue_PEW:
            py.draw.circle(screen, (153, 153, 0), (ammo_x, ammo_y), 2)

        ### RYS. GŁOWKI
        if red_left:
            cat_l(red_body_x-20,red_body_y-40)
        else:
            cat_p(red_body_x - 20, red_body_y - 40)
        if blue_left:
            doge_l(blue_body_x - 20, blue_body_y - 40)
        else:
            doge_p(blue_body_x - 20, blue_body_y - 40)

        ### BRONIE i celownik
        ##czerw celownik
        # dla czerwonego gracza
        if red_shoot_mode:
            if BAZOOKA:
                screen.blit(bazooka, (red_body_x-10, red_body_y-10))
            else:
                screen.blit(snipe, (red_body_x-10, red_body_y-10))
            if red_left:
                py.draw.line(screen, (255, 0, 0), (red_body_x, red_body_y),
                            (red_body_x- (dl_celownika*math.cos(2*math.pi*red_shoot_angle/360)), red_body_y - (dl_celownika*math.sin(2*math.pi*red_shoot_angle/360))))
            else:
                py.draw.line(screen, (255, 0, 0), (red_body_x, red_body_y),
                            ( red_body_x + (dl_celownika * math.cos(2 * math.pi * red_shoot_angle / 360)),red_body_y - (dl_celownika * math.sin(2 * math.pi * red_shoot_angle / 360))))
        # dla niebieskiego gracza
        if blue_shoot_mode:
            if BAZOOKA:
                screen.blit(bazooka, (blue_body_x-10, blue_body_y-10))
            else:
                screen.blit(snipe, (blue_body_x-10, blue_body_y-10))
            if blue_left:
                py.draw.line(screen, (255, 0, 0), (blue_body_x, blue_body_y),
                            (blue_body_x- (dl_celownika*math.cos(2*math.pi*blue_shoot_angle/360)), blue_body_y - (dl_celownika*math.sin(2*math.pi*blue_shoot_angle/360))))
            else:
                py.draw.line(screen, (255, 0, 0), (blue_body_x, blue_body_y),
                            ( blue_body_x + (dl_celownika * math.cos(2 * math.pi * blue_shoot_angle / 360)),blue_body_y - (dl_celownika * math.sin(2 * math.pi * blue_shoot_angle / 360))))

        ##sila strzalu
        # dla czerwonego gracza
        if red_shoot_start:
            dlug = dl_celownika * (red_shoot_v0 / max_shoot_speed)
            if red_left:
                py.draw.line(screen, (0, 0, 255), (red_body_x, red_body_y),
                             (red_body_x - (dlug * math.cos(2 * math.pi * red_shoot_angle / 360)),
                              red_body_y - (dlug * math.sin(2 * math.pi * red_shoot_angle / 360))))
            else:
                py.draw.line(screen, (0, 0, 255), (red_body_x, red_body_y),
                             (red_body_x + (dlug * math.cos(2 * math.pi * red_shoot_angle / 360)),
                              red_body_y - (dlug * math.sin(2 * math.pi * red_shoot_angle / 360))))
        # dla niebieskiego gracza
        if blue_shoot_start:
            dlug = dl_celownika * (blue_shoot_v0 / max_shoot_speed)
            if blue_left:
                py.draw.line(screen, (0, 0, 255), (blue_body_x, blue_body_y),
                             (blue_body_x - (dlug * math.cos(2 * math.pi * blue_shoot_angle / 360)),
                              blue_body_y - (dlug * math.sin(2 * math.pi * blue_shoot_angle / 360))))
            else:
                py.draw.line(screen, (0, 0, 255), (blue_body_x, blue_body_y),
                             (blue_body_x + (dlug * math.cos(2 * math.pi * blue_shoot_angle / 360)),
                              blue_body_y - (dlug * math.sin(2 * math.pi * blue_shoot_angle / 360))))

        ## efekt eksplozji

        if BUM == True:
            screen.blit(Exp[round(exp_ani)], (exp_x - 45, exp_y - 45))

        if BUM2 ==True:
            screen.blit(Exp[round(exp_ani)], (exp_min_x - 45, exp_min_y - 45))

        # Wygrana meczu
        if red_HP == 0 and blue_score == 2:
            screen.blit(pies_win, (490, 215))
            if event.type == py.KEYDOWN:
                sys.exit(0)
        if blue_HP == 0 and red_score ==2:
            screen.blit(kot_win, (490, 215))
            if event.type == py.KEYDOWN:
                sys.exit(0)

        ## BARY ZYCIA ITP

        cat_p(0, 680)
        doge_l(1280-40, 680)
        RED_HP_podst = py.Rect(40, 690, 200, trawa_wysokosc /2)
        BLUE_HP_podst = py.Rect(1280-240, 690, 200, trawa_wysokosc / 2)
        RED_HP = py.Rect(40,690,200*red_HP/100,trawa_wysokosc/2)
        BLUE_HP = py.Rect(1280-240+200*(1-blue_HP/100),690,200*blue_HP/100,trawa_wysokosc/2)

        py.draw.rect(screen, (144,96,48), RED_HP_podst)
        py.draw.rect(screen, (144,96,48), BLUE_HP_podst)

        py.draw.rect(screen, (255, 0, 0), RED_HP)
        py.draw.rect(screen, (0, 0, 255), BLUE_HP)

        # CZAS
        if red_turn:
            screen.blit(lzero, (1280 - 50, 50))
            screen.blit(liczby[max_turn_time - 1 - math.floor(red_turn_time)], (50, 50))
        else:
            screen.blit(lzero, (50, 50))
            screen.blit(liczby[max_turn_time - 1 - math.floor(blue_turn_time)], (1280 - 50, 50))

        if red_score==0 and blue_score==0:
            screen.blit(score_0_0,(610,685))
        elif red_score==1 and blue_score==0:
            screen.blit(score_1_0,(610,685))
        elif red_score==0 and blue_score==1:
            screen.blit(score_0_1,(610,685))
        elif red_score == 1 and blue_score == 1:
            screen.blit(score_1_1, (610, 685))
        elif red_score == 1 and blue_score == 2:
            screen.blit(score_1_2, (610, 685))
        elif red_score == 2 and blue_score == 1:
            screen.blit(score_2_1, (610, 685))
        elif red_score == 2 and blue_score == 2:
            screen.blit(score_2_2, (610, 685))
        elif red_score == 2 and blue_score == 0:
            screen.blit(score_2_0, (610, 685))
        elif red_score == 0 and blue_score == 2:
            screen.blit(score_0_2, (610, 685))

        py.display.flip()

