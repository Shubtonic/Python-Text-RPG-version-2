import random
import time
import os


class Hero(object):
    def __init__(self):
        self.level = 1
        self.max_hp = 10
        self.hp = self.max_hp
        self.attack = 10 + self.level
        self.defense = 5 + self.level
        self.name = ''
        self.xp = 0
        self.mana = 5 +self.level
        self.class_p = ""


    def name_self(self):
        self.name = input("What do you call yourself, anyway? ")
        if self.name == "":
            self.name_self()
        Hero.class_self(self)

    def class_self(self):
        print("Player class\n_____________\nTHEIF\nWARRIOR\nMAGE\nARCHERY\n")
        self.class_p = input("What is you class?").lower()
        if self.class_p == "":
            print("HAHAHA Someone is being brave. ")
            time.sleep(1)
        elif self.class_p == "mage":
            print("Let me guess. You have a 'Magical' personality.", [self.mana + 5])
            time.sleep(1)
        elif self.class_p == "theif":
            print("Hey! Don't touch my gold!", [self.hp + 5])
            time.sleep(1)
        elif self.class_p == "warrior":
            print("So... Can your sword cut through butter?", [self.defence + 5])
            time.sleep(1)
        else:
            os.system('cls')
            Hero.class_self(self)

    def heal_self(self):
        amount = self.xp * .2
        self.hp += amount
        print("You attempt to heal yourself...")
        time.sleep(1)
        print("You healed yourself for %d HP, but used half your XP. Feels good, man." % (amount))
        self.xp *= .5
        self.hp_limit()

    def hp_limit(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp


    def death(self):
        print("Sorry, %s, you is dead now." % (self.name))
        time.sleep(1)
        print("Well, aren't you lucky, there is an afterlife after all.")


    def xp_up(self, xp):
        self.xp += xp
        print("You gain: %s XP" % (xp))


    def look_self(self):
        print ("\n\nYou find yourself in your humble abode.\n Well..... \n That is the only good thing about it.") #% self.name)
        print ("[Experience Points needed: %s ]" % (self.level**2 * 10))

class Monster(object):
    def __init__(self, name):
        self.name = name
        self.hp = random.randint(2,10)
        self.attack = random.randint(2,5)
        self.defense = random.randint(2,5)
        self.xp = random.randint(2,8)


class NPC(object):
    def __init__(self, name):
        self.name = name
        self.hp = random.randint(2,10)
        self.attack = random.randint(2,5)
        self.defense = random.randint(2,5)
        self.xp = random.randint(2,8)
        self.questNum = random.randint(1,8)


class Room:
    def __init__(self, key):
        self.room_data = {
            "home":{"description":"This is where you live, unfortunately.",
                    "exits":["forest"]},
            "forest":{"description":"You're in a dark forest. It's fairly gloomy.",
                    "exits":["home", "lake"]},
            "lake":{"description":"You see a lake circled by rocks. It's too cold to swim.",
                    "exits":["forest","mountain"]},
            "mountain":{"description":"You can see for miles around. Don't fall off.",
                    "exits":["lake"]},
            "Volcanic Plume":{"description":"Fire churns and burns in this desolite land",
                    "exits":["mountain"]}
            }
        self.description = self.room_data[key]["description"]
        self.exits = self.room_data[key]["exits"]
        self.name = str(key)
        self.monster_list = {}


class Game:
    def __init__(self):
        self.command_list = ["look","name","fight","heal",'report','move','?']
        self.hero = Hero()
        self.current_room = Room("home")



    def list_commands(self):
        print('Commands are', ', '.join(self.command_list[:-1]), 'and', self.command_list[-1] + '.')


    def handle_input(self):
        com = input(self.prompt()).lower().split()
        if len(com) < 1:
            print ("Huh?")
        elif com[0] == "fight":
            if len(com) > 1:
                if com[1] in self.current_room.monster_list:
                    self.combat(self.hero, self.current_room.monster_list[com[1]])
            else:
                print("Fight what?")
        elif com[0] == "report":
            self.hero.look_self()
        elif com[0] == "look":
            if len(com) > 1:
                if com[1] in self.current_room.monster_list:
                    self.look_monster(self.current_room.monster_list[com[1]])
                else:
                    print("You don't see that monster.")
            else:
                self.look()
        elif com[0] == "move":
            if len(com) > 1:
                self.move(com[1])
            else:
                print("Move where?", "You can exit to: %s" % ', '.join(self.current_room.exits))
        elif com[0] == "name":
            self.hero.name_self()
        #elif com[0] == "info":
         #   self.info()
        elif com[0] == "heal":
            self.hero.heal_self()
        elif com[0] == "?":
            self.list_commands()
        elif com[0] == "help":
            self.list_commands()
        else:
            print("lol wut")


    def combat(self, attacker, defender):
        print("%s Vs %s" % (attacker.name.capitalize(),defender.name.capitalize()))
        print("")
        while defender.hp > 0 and attacker.hp > 0:
            attack = int(random.random() * attacker.attack)
            defense = int(random.random() *defender.defense)
            print("/n%s Vs %s" % (attacker.name.capitalize(),defender.name.capitalize()))
            #print("Attack: %s vs Defense: %s" % (str(attack), str(defense)))
            if attack > defense:
                print("You hit the %s for %s HP." % (defender.name.capitalize(), str(attack)))
                defender.hp -= attack
            elif attack == defense:
                print("The attack missed. You feel kind of disappointed.")
            else:
                print ("The %s hit you for %s HP" % (defender.name.capitalize(), str(attack)))
                self.hero.hp -= attack
                if self.hero.hp < 2:
                    print("You attempt to escape...")
                    time.sleep(1)
                    break
            time.sleep(.5)
        if defender.hp < 1:
            print("You killed the %s. How sad for the %s's family." % (defender.name.capitalize(), defender.name.capitalize()))
            self.hero.xp_up(defender.xp)
            del self.current_room.monster_list[defender.name]
        if self.hero.hp < 1:
            self.hero.death()



    def level_up(self):
        if self.hero.xp > self.hero.level**2 * 10:
            self.hero.level += 1
            print ("You've reached level " + str(self.hero.level))
            self.hero.max_hp += self.hero.level
            self.hero.hp = self.hero.max_hp


    def populate(self):
        for i in range(self.hero.level):
            new_monster = random.choice(["ogre", "orc", "goblin"])
            self.current_room.monster_list[new_monster] = Monster(new_monster)


    def look(self):
        print(self.current_room.description)
        print("We can exit to: %s" % ', '.join(self.current_room.exits))
        monster_list= []
        for name in self.current_room.monster_list:
            monster_list.append(self.current_room.monster_list[name].name.capitalize())
        if monster_list:
            print("You see: %s" % ', '.join(monster_list))


    def look_monster(self, monster):
         (look_monster % (monster.name.capitalize(), monster.hp, monster.attack, monster.defense, monster.xp))


    def move(self, exit):
        if exit in self.current_room.exits:
             self.current_room = Room(exit)
             self.populate()
             self.look()
        elif exit == self.current_room.name:
            print ("We're already here.")
        else:
            print("There is not a route to go there...")


    def update(self):
        self.level_up()
        if self.hero.hp <= 0:
            self.hero.death()
            time.sleep(2)
            game = Game()


    def prompt(self):
        return '\n' + self.hero.name + " HP:" + str(self.hero.hp) + " XP:" + str(self.hero.xp) + " Class:" + self.hero.class_p + ">"


    def PlayerIntro(self):
        print("\n")
        print("====================")
        print("  Dark Skcar'Mara")
        print("====================")
        print("\n")


    def output(self):
        pass

       # print("test")

game = Game()

game.populate()
game.PlayerIntro()
print("Welcome, adventurer.")
game.list_commands()
game.hero.name_self()
game.hero.look_self()
game.look()

while True:
    game.handle_input()
    game.update()
    game.output()
