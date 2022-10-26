from email import message
import random
robot_art = r"""
0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/        
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}
                                
"""
colors = {
        "black": '\x1b[90m',
        "blue": '\x1b[94m',
        "white": '\x1b[97m',
        "yellow" : "\x1b[93m",
        "red" : "\x1b[91m",
    "light_green" : "\033[1;32m",
    "bold" : "\033[1m",
    "dark_gray" : "\033[1;30m",
}

class Part():
    
    def __init__(self, name: str, attack_level=0, defense_level=0, energy_consumption=0):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption

    def get_status_dict(self):
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name): self.defense_level,
            "{}_energy_consump".format(formatted_name): self.energy_consumption,
        }
        
    def is_available(self):
        return self.defense_level >= 0
#Esta parte esta disponible siempre cuando tengaamos defensa ,sea <= 0
class Robot:
    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code.lower()
        self.energy = 100
        self.weaponCounter = 0
        self.shieldCounter = 0
        self.hasShield = False
        self.parts = [
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
            Part("Weapon", attack_level=15, defense_level=0, energy_consumption=10),
            Part("Left Arm", attack_level=10, defense_level=0, energy_consumption=10),
            Part("Right Arm", attack_level=6, defense_level=10, energy_consumption=10),
            Part("Left Leg", attack_level=4, defense_level=10, energy_consumption=15),
            Part("Right Leg", attack_level=8, defense_level=5, energy_consumption=15),
        ]
    def canUseWeapon(self):
      return self.weaponCounter < 2

    def canUseShield(self):
      return self.shieldCounter < 1

    def useWeapon(self):
      self.weaponCounter += 1

    def useShield(self):
      self.hasShield = True
      self.shieldCounter += 1

    def greet(self):
      print("Hello,my name is", self.name)
    
    def print_energy(self):
      print("We have", self.energy, "percent energy left")

    def attack(self, enemy_robot, part_to_use, part_to_attack):
      if enemy_robot.hasShield:
        enemy_robot.hasShield = False
      else:
        enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level

      self.energy -= self.parts[part_to_use].energy_consumption
   
    def is_on(self):
      return self.energy > 0

    def is_there_available_part(self):
      for part in self.parts:
        if part.is_available():
          return True
      return False

    def getOptions(self):
      res = "Select an option:\n1 Normal attack"
      if self.canUseWeapon():
        res += "\n2 Weapon attack"
      if self.canUseShield():
        res += "\n3 Use shield"
      res += "\n"
      return res

#imprimos las partes de nuestro robot con un color asignado,creamos nuevo metodo   
    def print_status(self):
        print(self.color_code)
        str_robot = robot_art.format(**self.get_part_status())
        self.greet()
        self.print_energy()
        print(str_robot)
        print(colors["black"])
    
#actualizamos el metodo diccionario ,con un elemto(objeto)
#unimos self.parts con get_status_dict,que retorna par_status
    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            status_dict = part.get_status_dict()
            part_status.update(status_dict)
        return part_status
#Esta funcion nos servira crear el robot
# e implementar el nombre del robot que nos dara el usuario
def build_robot():
    robot_name = input("Robot name: ")
    color_code = choose_color()
    robot = Robot(robot_name, color_code)
    robot.print_status()
    return robot

#cada jugador que tenga un color distinto y el usuario o jugador pueda escoger ese color,por consola,con input
def choose_color():
    available_colors = colors
    print("Available colors:")
    for key, value in available_colors.items():
        print(value, key)
    print(colors["blue"])
    chosen_color = input("Choose a color: ")
    color_code = available_colors[chosen_color]
    return color_code

def readNumber(message):
  return int(input(message))

def normalAttack(current_robot, enemy_robot):
  current_robot.print_status()
  print("What part should I use to attack?")
  part_to_use = -1
  while True:
    part_to_use = int(input("Choose a number part: "))
    if part_to_use == 1:
      print("You can not select a weapon in normal attack")
    else:
      break

  enemy_robot.print_status()
  print("Which part of the enemy should we attack?")
  part_to_attack = int(input("Choose a enemy part to attack:"))

  current_robot.attack(enemy_robot, part_to_use, part_to_attack)

def weaponAttack(current_robot, enemy_robot):
  enemy_robot.print_status()
  print("Which part of the enemy should we attack?")
  part_to_attack = int(input("Choose a enemy part to attack:"))
  weaponIndex = 1
  current_robot.useWeapon()
  current_robot.attack(enemy_robot, weaponIndex, part_to_attack)

#funcion global (jugar)
def play():
  playing = True
  print("Welcome to the Game!")
  print("Data for Player 1>")
  robot_one = build_robot()
  print("Data for Player 2>")
  robot_two = build_robot()
  round = 0
  while playing:
    turn = random.randint(0,9)
    if turn % 2 == 0:
      current_robot = robot_one
      enemy_robot = robot_two
    else:
      current_robot = robot_two
      enemy_robot = robot_one
    
    while True:
      print("Attacker is: "+current_robot.name)
      option = readNumber(current_robot.getOptions())
      if option == 1:
        normalAttack(current_robot, enemy_robot)
        break
      elif option == 2:
        if current_robot.canUseWeapon():
          weaponAttack(current_robot, enemy_robot)
          break

      elif option == 3:
        if current_robot.canUseShield():
          current_robot.useShield()
          break
      print("Invalid option")
    
    round += 1

    if (not enemy_robot.is_on()) or (enemy_robot.is_there_available_part() == False):
      playing = False
      print("Congratulations you won¡¡¡")
      print(current_robot.name)

play()

