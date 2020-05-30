#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 08:48:24 2020

@author: BlackBox
"""

import discord
from discord.ext import commands,tasks
import os
import sys
import time
from itertools import cycle
import random

client = commands.Bot(command_prefix="!") #prefix may be changed to whatever you want so long as the command names are
GUILD = 'exampleGuild' #server name
TOKEN = 'exampleToken' #bot token
PASS = 'toor'

@client.event #connect
async def on_connect():
    print('connected')

@client.event #startup
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('Waiting'))
    print('ready')
    

@client.command() #shutdown
@commands.has_permissions(administrator=True)
async def quit(ctx):
    print('shutting down')
    await ctx.send('Shutting Down')
    sys.exit()

votingLog = []
notEligible = []
playerList = {}
policyTiles = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1]
liberalPolicies = 0
fascistPolicies = 0
jaVotes = 0
neinVotes = 0
failedElections = 0
fakePlayers = 0
elected = 0
fboard = 0

class Player:
    def __init__(self,order,handle,discordID,faction,isChancellor,isPresident,isHitler,isAlive):
        self.order = order
        self.handle = handle
        self.discordID = discordID
        self.faction = faction
        self.isChancellor = isChancellor
        self.isPresident = isPresident
        self.isHitler = isHitler
        self.isAlive = isAlive
    
@client.command()
async def ready(ctx,*,username):
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            await ctx.send('Already registered')
            return
    playerCount = len(playerList)
    await ctx.send('{} is ready'.format(username))
    print(ctx.author)
    newPlayer = Player(playerCount,username,ctx.author,'unassigned',False,False,False,False)
    playerList['player{}'.format(playerCount)] = newPlayer

@client.command()
async def unReady(ctx):
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            await ctx.send('Removing player')
            playerList.pop(n)
            return
    await ctx.send('Player not listed as ready')

@client.command()
async def listPlayers(ctx):
    if len(playerList) == 0:
        await ctx.send('There are no players ready')
    else:
        for n,player in playerList.items():
            print(n)
            print(player)
            await ctx.send('Username: {}, DiscordID: {}'.format(player.handle,player.discordID))

@client.command() 
@commands.has_permissions(administrator=True)
async def assignRoles(ctx):
    index = []
    for i in range(0,len(playerList)):
        index.append(i)
    index = random.shuffle(index)
    for n,player in playerList.items():
        #index out of range here
            if player.order == index[0]:
                player.faction = 'fascist'
                player.isHitler = True
            if player.order == index[1]:
                player.faction = 'fascist'
            if player.order == index[2]:
                player.faction = 'liberal'
            if player.order == index[3]:
                player.faction = 'liberal'
            if player.order == index[4]:
                player.faction = 'liberal'
            if player.order == index[5]:
                player.faction = 'liberal'
            if player.order == index[6]:
                player.faction = 'fascist'
            if player.order == index[7]:
                player.faction = 'liberal'
            if player.order == index[8]:
                player.faction = 'fascist'
            if player.order == index[9]:
                player.faction = 'liberal'

@client.command()
@commands.has_permissions(administrator=True)
async def pmRoles(ctx):
    for n,player in playerList.items():
        if player.faction == 'liberal':
            await player.discordID.create_dm()
            await player.discordID.dm_channel.send('You are a liberal. You must find Hitler and prevent him from taking power')
        if player.faction == 'fascist':
            await player.discordID.create_dm()
            await player.discordID.dm_channel.send('You are a fascist. ')
            if player.isHitler == True:
                hitlerPlayer = player
    for n,player in playerList.items():
        if player.faction == 'fascist':
            await player.discordID.create_dm()
            await player.discordID.dm_channel.send('You must ensure {} rises to power.'.format(hitlerPlayer.handle))
    
@client.command() 
@commands.has_permissions(administrator=True)
async def startGame(ctx):
    global policyTiles
    global fboard
    if fboard < 7:
        fboard = 1
    if fboard > 8:
        fboard = 3
    if (fboard == 7) or (fboard == 8):
        fboard = 2
    policyTiles = random.shuffle(policyTiles)
    if len(playerList) < 5:
        ctx.send('Too few players')
        #return
        pass
    if len(playerList) > 10:
        ctx.send('Too many players')
        #return
        pass
    await ctx.send('Starting Game!')
    time.sleep(2)
    for n,player in playerList.items():
        if player.order == 0:
            player.isPresident = True
            await ctx.send('{} is the First President and may nominate a chancellor'.format(player.handle))
            time.sleep(1)
            await ctx.send('Type !nominate handle, ie !nominate bob')

@client.command()
async def nominate(ctx,*,nominee):
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            if player.isPresident == False:
                await ctx.send('{} is not president!'.format(player.handle))
                return
    for n,player in playerList.items():
        if nominee == player.handle:
            if player.isAlive == False:
                await ctx.send('{} is dead!'.format(nominee))
            if nominee in notEligible:
                await ctx.send('{} was in the previous goverment. They are not eligible!'.format(nominee))
                return
            else:
                await ctx.send('Voting on Chancellor {} opens now. Type !vote Ja or !vote Nein, and !countVotes when the votes are in'.format(nominee))
                await ctx.send('You may direct message votes to the bot')
                player.isChancellor == True
        else:
            await ctx.send('Nominee not found. Try !listPlayers to check for handles')
            return
        
@client.command()
async def vote(ctx,*,vote):
    vote = vote.lower()
    global jaVotes
    global neinVotes
    for n,player in playerList.items():
        if ctx.author in votingLog:
            await ctx.send('You have already voted')
            return
        else:
            await ctx.send("{}'s vote registered".format(player.handle))
    if (vote == "ja") or (vote == 'ja!'):
        jaVotes += 1
        votingLog.append([ctx.author,vote])
    if (vote == "nein") or (vote == 'na!'):
        neinVotes += 1
        votingLog.append([ctx.author,vote])

@client.command()
async def countVotes(ctx):
    global jaVotes
    global neinVotes
    global elected
    global failedElections
    global votingLog
    if (neinVotes + jaVotes) == len(playerList):
        votingLog = []
        if jaVotes > neinVotes:
            await ctx.send('Goverment elected! President may use !policy to enact policy')
            elected = 1
            notEligible = []
            for n,player in playerList.items():
                if player.isPresident == True:
                    notEligible.append(player.handle)
                if player.isChancellor == True:
                    notEligible.append(player.handle)
        else:
            failedElections += 1
            elected = 0
            await ctx.send('Election Failed!')
            if failedElections == 3:
                #enact random policy
                pass
            for n,player in playerList.items():
                if player.isChancellor == True:
                    player.isChancellor = False
                if player.isPresident == True:
                    presNum = player.order
                    for n,player in playerList.items():
                        if presNum == len(playerList):
                            if player.isPresident == True:
                                player.isPresident = False
                                for n,player in playerList():
                                    if player.order == 0:
                                            await ctx.send('{} is the new president and may !nominate the new chancellor'.format(player.handle))
                                            player.isPresident = True
                        else:
                            if player.order == (presNum+1):
                                player.isPresident = True
                                await ctx.send('{} is the new president and may !nominate the new chancellor'.format(player.handle))
                        
    else:
        await ctx.send('Not enough votes yet')
        
presIsDone = False
handTrans = []

@client.command()
async def policy(ctx):
    if len(policyTiles) < 3:
        await ctx.send('Make sure to !shuffle policy tiles before drawing')
    for n,player in playerList.items():
        if player.discordID == ctx.author:
            if player.isPresident == True:
                hand = []
                hand.append(policyTiles.pop(0))
                hand.append(policyTiles.pop(0))
                hand.append(policyTiles.pop(0))
                global handTrans
                handTrans = []
                for num in hand:
                    if num == 0:
                        handTrans.append('liberal policy')
                    if num == 1:
                        handTrans.append('fascist policy')
                await player.discordID.create_dm()
                await player.discordID.dm_channel.send('Polices to choose from:')
                await player.discordID.dm_channel.send('{}'.format(handTrans))
                await player.discordID.dm_channel.send('Use !discard # to discard a tile in order, ie !discard 1')
                return
            else:
                await ctx.send('You are not president')
                return

@client.command()
async def discard(ctx, * ,choice):
    for n,player in playerList.items():
        if player.discordID == ctx.author:
            if player.isPresident == False:
                await ctx.send('Only the president can discard')
                return
    global handTrans
    global presIsDone
    if choice == '1':
        handTrans.pop(0)
    if choice == '2':
        handTrans.pop(1)
    if choice == '3':
        handTrans.pop(2)
    presIsDone = True
    await ctx.send('The President has chosen. Waiting for the Chancellor to enact a policy.')
    for n,player in playerList.items():
        if player.isChancellor == True:
            await player.discordID.create_dm()
            await player.discordID.dm_channel.send('Polices to choose from:')
            await player.discordID.dm_channel.send('{}'.format(handTrans))
            await player.discordID.dm_channel.send('Use !choose #, ie !choose 1')
govermentActionCanBeTaken = False
canExamine = False
canKill = False
canSpecialElection = False
canInvestigate = False

@client.command()
async def choose(ctx, * , choice):
    global govermentActionCanBeTaken
    global presIsDone
    global fascistPolicies
    global liberalPolicies
    global canExamine
    global canInvestigate
    global canKill
    global canSpecialElection
    enacted = []
    for n,player in playerList.items():
        if player.discordID == ctx.author:
            if player.isChancellor == False:
                await ctx.send('Only the Chancellor can choose')
                return
    if presIsDone == False:
        ctx.send('The President is not done.')
        return
    else:
        if choice == '1':
            enacted.append(handTrans.pop(0))
        if choice == '2':
            enacted.append(handTrans.pop(1))
        if enacted == 'fascist':
            fascistPolicies += 1
            if liberalPolicies == 6:
                await ctx.send('Fascist Victory! Oh no!')
                await ctx.send('Use !endGame to end game')
            await ctx.send('A fascist policy has been enacted!')
            if fboard == 1:
                if fascistPolicies == 3:
                    await ctx.send('The President must examine policies with !examine')
                    canInvestigate = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 4:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 5:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
            if fboard == 2:
                if fascistPolicies == 2:
                    await ctx.send('The President must investigate with !investigate')
                    canInvestigate = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 3:
                    await ctx.send('A special election must be held! Use !specialElection')
                    canSpecialElection = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 4:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 5:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
            if fboard == 3:
                if fascistPolicies == 1:
                    await ctx.send('The President must investigate with !investigate')
                    canInvestigate = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 2:
                    await ctx.send('The President must investigate with !investigate')
                    canInvestigate = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 3:
                    await ctx.send('A special election must be held! Use !specialElection')
                    canSpecialElection = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 4:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
                if fascistPolicies == 5:
                    await ctx.send('The President must kill with !kill')
                    canKill = True
                    govermentActionCanBeTaken = True
        if enacted == 'liberal':
            liberalPolicies += 1
            if liberalPolicies == 6:
                await ctx.send('Liberal Victory!')
                await ctx.send('Use !endGame to end game')
            await ctx.send('A liberal policy has been enacted')
        await ctx.send('Someone may type !nextRound to send the round once discussion of the policy is over and goverment action has been taken')
#Goverment actions will go here
        
@client.command()
async def investigate(ctx,*,member):
    global govermentActionCanBeTaken
    if govermentActionCanBeTaken == False:
        await ctx.send('There is no goverment action to be taken right now')
        return
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            if player.isPresident == False:
                await ctx.send('You are not president!')
    global canInvestigate
    if canInvestigate == True:
        for n,player in playerList.items():
            if member == player.handle:
                await ctx.author.create_dm()
                await ctx.author.dm_channel.send('{} is a {}'.format(player.handle,player.faction))
                govermentActionCanBeTaken = False
                canInvestigate = False
                return
            else:
                await ctx.send('No player found')
                return
    else:
        await ctx.send('You do not have this power right now!')
        return
    
@client.command()
async def kill(ctx,*,member):
    global govermentActionCanBeTaken
    if govermentActionCanBeTaken == False:
        await ctx.send('There is no goverment action to be taken right now')
        return
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            if player.isPresident == False:
                await ctx.send('You are not president!')
    global canKill
    if canKill == True:
        for n,player in playerList.items():
            if member == player.handle:
                playerList.pop(n)
                await ctx.send('The goverment has executed {}!'.format(player.handle))
                newOrder = 0
                for n,player in playerList.items():
                    player.order = newOrder
                    newOrder += 1
                govermentActionCanBeTaken = False
                canKill = False
            else:
                await ctx.send('No player found')
                return
    else:
        await ctx.send('You do not have this power right now!')
        return
    
@client.command()
async def specialElection(ctx,*,member):
    global govermentActionCanBeTaken
    if govermentActionCanBeTaken == False:
        await ctx.send('There is no goverment action to be taken right now')
        return
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            if player.isPresident == False:
                await ctx.send('You are not president!')
    global canSpecialElection
    if canSpecialElection == True:
        for n,player in playerList.items():
            if member == player.handle:
                 player.isPresident = True
                 await ctx.send('{} is the new president!'.format(player.handle))
                 govermentActionCanBeTaken = False
                 canSpecialElection = False
            else:
                    await ctx.send('No player found')
                    return
    else:
        await ctx.send('You do not have this power right now!')
        return

@client.command()
async def examine(ctx):
    global govermentActionCanBeTaken
    if govermentActionCanBeTaken == False:
        await ctx.send('There is no goverment action to be taken right now')
        return
    for n,player in playerList.items():
        if ctx.author == player.discordID:
            if player.isPresident == False:
                await ctx.send('You are not president!')
    global canExamine
    if canExamine == True:
        await ctx.author.create_dm()
        newPolicies = []
        global policyTiles
        for policy in policyTiles:
            if policy == 0:
                newPolicies.append('Liberal')
            if policy == 1:
                newPolicies.append('Fascist')
        await ctx.author.dm_channel.send('Next policies:')
        await ctx.author.dm_channel.send('{},{},{}'.format(newPolicies))
    else:
        await ctx.send('You do not have this power right now!')
        return

@client.command()
async def nextRound(ctx):
    global govermentActionCanBeTaken
    global notEligible
    if govermentActionCanBeTaken == True:
        await ctx.send('The goverment still needs to take action!')
        return
    else:
        await ctx.send('A new goverment will seek election!')
        for n,player in playerList.items():
            if player.isPresident == True:
                notEligible.append(player.handle)
            if player.isChancellor == True:
                notEligible.append(player.handle)
        for n,player in playerList.items():
                if player.isChancellor == True:
                    player.isChancellor = False
                if player.isPresident == True:
                    n = player.order
                    for n,player in playerList.items():
                        if player.order == len(playerList):
                            if player.isPresident == True:
                                for n,player in playerList():
                                    if player.order == 0:
                                        await ctx.send('{} is the new president and may !nominate the new chancellor'.format(player.handle))
                                        player.isPresident == True
                        if player.order == (n+1):
                            player.isPresident == True
                            await ctx.send('{} is the new president and may !nominate the new chancellor'.format(player.handle))

#!endGame once policies have been done            
            
                
            
client.run(TOKEN)