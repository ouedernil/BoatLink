#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Leila Ouederni"
__copyright__ = "HEIAFR 2017, Project BoatLink for HYDROcontest"
__credits__ = ["Leila Ouederni"]
__version__ = "1"
__email__ = "ouederni.l@gmail.com"
__status__ = "Prototype"

import time
import threading
import queue
import communication
import database
import os, sys
import random
import time
import json

JSON_PARAMETRES = os.path.join(os.getcwd(), '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/parametres.json')
JSON_STATUS = os.path.join(os.getcwd(), '/home/renard/Desktop/virtualenv/venv/boatLinkDatabase/key.json')
orderLive = ["tension_batterie", "tension_boost", "courant_batterie", "courant_max_moteur", "courant_moteur","capacite_totale_batterie","capacite_dispo_pourc","puissance_inst_moteur","temps_course_possible", "vitesse_bateau","heure","minute","seconde","erreur1", "erreur2","erreur3", "erreur4","erreur5","emergency_stop", "mode_stop_on","mode_man_course_end","mode_avant_stop_arr","accel_x","accel_y","accel_z"]
orderInit = ["tension_batterie", "tension_boost", "courant_batterie", "courant_max_moteur", "courant_moteur", "capacite_totale_batterie", "capacite_dispo_batterie","capacite_dispo_pourc","puissance_inst_moteur","temps_course_possible", "vitesse_bateau", "distance_parc_leger","distance_parc_lourd","vitesse_min_calc_temps","heure","minute","seconde","jour","mois","annee","erreur1", "erreur2","erreur3", "erreur4","erreur5","emergency_stop", "mode_stop_on","mode_man_course_end", "mode_avant_stop_arr","pos_foils1", "pos_foils2",  "pos_capteur_moteur1",  "pos_capteur_moteur2", "accel_x", "accel_y", "accel_z","reg_P_gouvernail", "reg_I_gouvernail", "reg_P_foils1", "reg_I_foils1", "reg_P_foils2", "reg_I_foils2", "reg_P_cour_moteur", "reg_I_cour_moteur"]

class readXbee(threading.Thread):
    def __init__(self, comXbee, awaitingChars):
        """
        Function: __init__
        --------------------------
        Construct a new readXbee thread
        comXbee: communication object
    	awaitingCharg: queue
        """
        threading.Thread.__init__(self)
        self.awaitingChars = awaitingChars
        self.comXbee = comXbee


    def run(self):
        """
        Function: run
        --------------------------
        Run the thread reading communication data
        and add them in the queue
        """
        while(True):
            x=self.comXbee.getChar()
            self.awaitingChars.put(ord(x))


class parseData(threading.Thread):
    def __init__(self, awaitingChars, goodFrames):
        """
        Function: __init__
        --------------------------
        Construct a new parseData thread
    	awaitingCharg: queue
        goodFrames: queue

        """
        threading.Thread.__init__(self)
        self.preamble = True
        self.payload = 1
        self.counter = 1
        self.frame = []
        self.awaitingChars = awaitingChars
        self.goodFrames = goodFrames



    def run(self):
        """
        Function: run
        --------------------------
        Run the thread parsing data in the awaitingChars queue
        Construct the frame and add it in the goodFrames queue
        """
        while(True):
            if not self.awaitingChars.empty():
                data = self.awaitingChars.get()
                if self.preamble:
                    if (data == 170):
                        self.counter += 1
                        print(self.counter)
                    else:
                        self.counter = 1
                if (self.counter == 4):
                    self.preamble = False
                    self.counter = 1
                    frameType = self.awaitingChars.get()
                    frameLength = self.awaitingChars.get()
                    del self.frame[:]
                    self.frame.append(frameType)
                    for i in range(frameLength):
                        data = self.awaitingChars.get()
                        self.frame.append(data)
                    data = self.awaitingChars.get()
                    if(data == 85):
                        print(self.frame)
                        self.goodFrames.put(self.frame)
                    self.preamble = True


class addInDatabase(threading.Thread):

    def __init__(self,dbBoatLink, goodFrames, frameMessage):
        """
        Function: __init__
        --------------------------
        Construct a new addInDatabase thread
        dbBoatLink: database object
        goodFrames: queue
    	frameMessage: queue

        """
        threading.Thread.__init__(self)
        self.goodFrames = goodFrames
        self.dbBoatLink = dbBoatLink
        self.frameMessage = frameMessage

    def run(self):
        """
        Function: run
        --------------------------
        Run the thread adding frames in the database
        Construct the json and add it in the frame message queue
        """
        while (True):
            try:
                if not self.goodFrames.empty():
                    attribute = json.load(open(JSON_PARAMETRES))
                    frame = goodFrames.get()
                    if (frame[0] == 1):
                        newFrame = []
                        j = 1
                        for e in range(len(orderLive)):
                            attr = attribute[orderLive[e]]
                            if (attr["envoiC"] == 1):
                                val = 0
                                for i in range(attr["size"]):
                                    val += frame[j]
                                    if(i < attr["size"] - 1):
                                        val = val << 8 
                                    j += 1
                                newFrame.append(val)
                        year, month, day, hour, minute,sec = time.strftime("%Y,%m,%d,%H,%M,%S").split(',')
                        self.dbBoatLink.insertDataEnvoiContinu(newFrame[0], newFrame[1], newFrame[2], newFrame[3],
                                                               newFrame[4], newFrame[5], newFrame[6], newFrame[7],
                                                               newFrame[8], newFrame[9], newFrame[10], newFrame[11],
                                                               newFrame[12], newFrame[13], newFrame[14], newFrame[15],
                                                               newFrame[16],
                                                               newFrame[17], newFrame[18], newFrame[19], newFrame[20],
                                                               newFrame[21], newFrame[22], newFrame[23], newFrame[24])
                        print("Database ok")
                        
                        d = {'tension_batterie': newFrame[0], 'tension_boost': newFrame[1], 'courant_batterie': newFrame[2],
                             'courant_max_moteur': newFrame[3], 'courant_moteur': newFrame[4],
                             'capacite_totale_batterie': newFrame[5], 'capacite_dispo_pourc': newFrame[6],
                             'puissance_inst_moteur': newFrame[7], 'temps_course_possible': newFrame[8],
                             'vitesse_bateau': newFrame[9], 'heure': newFrame[10], 'minute': newFrame[11],
                             'seconde': newFrame[12], 'erreur1': newFrame[13], 'erreur2': newFrame[14], 'erreur3':
                                 newFrame[15], 'erreur4': newFrame[16], 'erreur5': newFrame[17],'emergency_stop': newFrame[18], 'mode_stop_on': newFrame[19],'mode_man_course_end': newFrame[20], 'mode_avant_stop_arr': newFrame[21], 'accel_x': newFrame[22],'accel_y': newFrame[23], 'accel_z': newFrame[24]}
                        self.frameMessage.put(d)

                    if (frame[0] == 2):
                        newFrame = []
                        j = 1
                        for e in range(len(orderInit)):
                            attr = attribute[orderInit[e]]
                            if (attr["envoiI"] == 1):
                                val = 0
                                for i in range(attr["size"]):
                                    val += frame[j]
                                    if(i < attr["size"] - 1):
                                        val = val << 8 
                                    j += 1
                                newFrame.append(val)
                        self.dbBoatLink.insertDataEnvoiInit(newFrame[0], newFrame[1], newFrame[2], newFrame[3], newFrame[4],
                                                            newFrame[5], newFrame[6], newFrame[7], newFrame[8], newFrame[9],
                                                            newFrame[10]*1000/3600, newFrame[11], newFrame[12],
                                                            newFrame[13], newFrame[14], newFrame[15], newFrame[16],
                                                            newFrame[17], newFrame[18], newFrame[19], newFrame[20],
                                                            newFrame[21], newFrame[22], newFrame[23], newFrame[24],
                                                            newFrame[25],
                                                            newFrame[26], newFrame[27], newFrame[28], newFrame[29],
                                                            newFrame[30], newFrame[31], newFrame[32], newFrame[33],
                                                            newFrame[34], newFrame[35],
                                                            newFrame[36], newFrame[37], newFrame[38], newFrame[39],
                                                            newFrame[40], newFrame[41], newFrame[42], newFrame[43])

                        d = {'tension_batterie': newFrame[0], 'tension_boost': newFrame[1], 'courant_batterie': newFrame[2],
                             'courant_max_moteur': newFrame[3], 'courant_moteur': newFrame[4],
                             'capacite_totale_batterie': newFrame[5], 'capacite_dispo_batterie': newFrame[6],
                             'capacite_dispo_pourc': newFrame[7], 'puissance_inst_moteur': newFrame[8],
                             'temps_course_possible': newFrame[9], 'vitesse_bateau': newFrame[10],
                             ' distance_parc_leger': newFrame[11], 'distance_parc_lourd': newFrame[12],
                             'vitesse_min_calc_temps': newFrame[13], 'heure': newFrame[14], 'minute': newFrame[15],
                             'seconde': newFrame[16], 'jour': newFrame[17], 'mois': newFrame[18], 'annee': newFrame[19],
                             'erreur1': newFrame[20], 'erreur2': newFrame[21], 'erreur3':
                                 newFrame[22], 'erreur4': newFrame[23], 'erreur5': newFrame[24],
                             'mode_man_course_end': newFrame[25], 'mode_avant_stop_arr': newFrame[26],
                             'emergency_stop': newFrame[27], 'mode_stop_on': newFrame[28], 'pos_foil1': newFrame[29],
                             'pos_foil2': newFrame[30], 'pos_capt_moteur1': newFrame[31], 'pos_capt_moteur2': newFrame[32],
                             'accel_x': newFrame[33], 'accel_y': newFrame[34], 'accel_z': newFrame[35],
                             'regul_P_gouv': newFrame[36], 'regul_I_gouv': newFrame[37], 'regul_P_foil1': newFrame[38],
                             'regul_I_foil1': newFrame[39], 'regul_P_foil2': newFrame[40], 'regul_I_foil2': newFrame[41],
                             'regul_P_courant_m': newFrame[42], 'regul_I_courant_m': newFrame[43]}
                        self.frameMessage.put(d)
            except IOError as e:
                print("I/O error({0}):{1}".format(e.errno, e.strerror))
            except ValueError:
                print("Could not convert data to an integer.")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise







###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
import queue
import json

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
from twisted.internet.threads import defer


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = payload.decode('utf8')
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, q):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.q = q
        print("INIT BROADCASTSERVERFACTORY") 
        reactor.callFromThread(self.setLiveData)

    def setLiveData(self):
        if not self.q.empty():
            jsonData = self.q.get()
            self.broadcast(json.dumps(jsonData)) 
        reactor.callInThread(self.setLiveData) 

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))



class BroadcastPreparedServerFactory(BroadcastServerFactory):

    """
    Functionally same as above, but optimized broadcast using
    prepareMessage and sendPreparedMessage.
    """

    def broadcast(self, msg):
        print("broadcasting prepared message '{}' ..".format(msg))
        preparedMsg = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(preparedMsg)
            print("prepared message sent to {}".format(c.peer))


if __name__ == "__main__":
    print('RUNNING')
    comXbee = communication.communication()
    dbBoat = database.boatDatabase()
    awaitingChars = queue.Queue()
    goodFrames = queue.Queue()
    frameMessage = queue.Queue()
    frameToBoat = queue.Queue()
    readData = readXbee(comXbee, awaitingChars)
    parseD = parseData(awaitingChars, goodFrames)
    addDb = addInDatabase(dbBoat, goodFrames, frameMessage)
    readData.start()
    parseD.start()
    addDb.start()

    print('SERVER RUNNING')
    log.startLogging(sys.stdout)
    ServerFactory = BroadcastServerFactory
    factory = ServerFactory(u"ws://160.98.31.214:2000", frameMessage)
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)
    webdir = File(".")
    web = Site(webdir)
    reactor.listenTCP(8080, web)
    reactor.run()


















