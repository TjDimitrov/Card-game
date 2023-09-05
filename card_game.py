import random
import time


def withdrawal(current_deck):
    current_deck = {}
    for _ in range(5):
        current_key = random.choice(list(all_cards_deck.keys()))
        current_deck[current_key] = all_cards_deck[current_key]
        del all_cards_deck[current_key]
    return current_deck


def valid_card(card):
    while card not in player_card_deck:
        if card == "Cards":
            print("\033[93mYou have in hand:\033[0m")
            for card in player_card_deck:
                print(card)
        else:
            print("There is no such card in our deck.")
        card = input()
    return card


def death_scythe_effect(enemy_health, card_hp):
    enemy_health -= 100
    card_hp += 100
    if card_hp > 700:
        card_hp = 700
    return enemy_health, card_hp


def shrapnel_mine_effect(enemy_health, enemy_card_hp):
    enemy_health -= 100
    enemy_card_hp -= 500
    return enemy_health, enemy_card_hp


def enemy_or_not(card):
    enemy = False
    ours = False
    if card in enemy_card_deck:
        enemy = True
    elif card in player_card_deck:
        ours = True
    return enemy, ours


def battle(attack_card, attacker, attacker_hp, defender_card, defender, defender_hp, turns):
    enemy_not_summoned = False
    ours_not_summoned = False
    attack_card_attack = attacker[attack_card][0]
    attack_card_hp = attacker[attack_card][1]
    defence_card_hp = defender[defender_card][1]
    if attack_card == "Death Scythe":
        defender_hp, attack_card_hp = death_scythe_effect(defender_hp, attack_card_hp)
        if attack_card in enemy_card_deck:
            print(f"\033[91mThe Reaper has touched your soul! You have left {player_hp - 100} health.\033[0m")
        elif attack_card in player_card_deck:
            print(f"\033[91mThe Reaper found new soul! Enemy health left {enemy_hp - 100}.\033[0m")
    elif attack_card == "Shrapnel Mine":
        defender_hp, defence_card_hp = shrapnel_mine_effect(defender_hp, defence_card_hp)
        print(f"Shrapnel Mine explodes dealing 700 damage!")
        time.sleep(1)
    elif attack_card == "The Trickster":
        if attacker[attack_card][2] == 1:
            turns += 1
            attacker[attack_card][2] -= 1
            if attack_card in player_card_deck:
                ours_not_summoned = enemy_or_not(attack_card)
            else:
                enemy_not_summoned = enemy_or_not(attack_card)
    if defender_card == "Succubus":
        attack_card_attack -= 200
    elif defender_card == "Shrapnel Mine":
        print(f"Shrapnel Mine has been triggered!")
        attacker_hp, attack_card_hp = shrapnel_mine_effect(attacker_hp, attack_card_hp)
        print(f"Shrapnel Mine explodes dealing 500 damage!")
        time.sleep(1)
    defence_card_hp -= attack_card_attack
    defender[defender_card][1] -= attack_card_attack
    if defence_card_hp <= 0:
        if defender_card in player_card_deck:
            ours_not_summoned = enemy_or_not(defender_card)
        else:
            enemy_not_summoned = enemy_or_not(defender_card)
        if defender_card != "Shrapnel Mine":
            print(f"{defender_card} is destroyed!")
        del defender[defender_card]
        defender_hp -= 200
    else:
        print(f"{attack_card} hits {defender_card} for {attack_card_attack}.")
    if attack_card_hp <= 0:
        if attack_card in player_card_deck:
            ours_not_summoned = enemy_or_not(attack_card)
        else:
            enemy_not_summoned = enemy_or_not(attack_card)
        if attack_card != "Shrapnel Mine":
            print(f"{attack_card} is destroyed!")
        del attacker[attack_card]
        attacker_hp -= 200
    return attacker_hp, defender_hp, turns, enemy_not_summoned, ours_not_summoned


# Starting players data
enemy_hp = 1000
player_hp = 1000
all_cards_deck = {"Dark Magician": [450, 600], "Death Scythe": [550, 500], "High Elf": [400, 490],
                  "Shrapnel Mine": [200, 0], "Giant Tortoise": [250, 700], "The Trickster": [350, 500, 1],
                  "Lizard General": [390, 500], "Snowman": [300, 450], "Succubus": [300, 470], "Viking": [430, 550]}
enemy_card_deck = {}
enemy_card_deck = withdrawal(enemy_card_deck)
player_card_deck = {}
player_card_deck = withdrawal(player_card_deck)

turn = random.randint(0, 2)

enemy_card_is_not_summoned = True
enemy_card = ''
player_card_is_not_summoned = True
chosen_card = ''

print("You have in hand:")
for cards in player_card_deck:
    print(cards)
print("...")
time.sleep(0.5)

while True:  # Battles
    if player_card_is_not_summoned:
        if turn % 2 == 1:
            print("You are attacking.")
        else:
            print("Prepare to defend!")
        print(f"\033[93mPick a card: \033[0m", end='')
        chosen_card = valid_card(input())
    if enemy_card_is_not_summoned:
        enemy_card = random.choice(list(enemy_card_deck.keys()))
        print(f"\033[94mEnemy has summoned {enemy_card}!\033[0m")
        time.sleep(1)
    if turn % 2 == 1:  # Attack
        print(f"{chosen_card} is attacking!")
        time.sleep(1)
        player_hp, enemy_hp, turn, enemy_card_is_not_summoned, player_card_is_not_summoned \
            = battle(chosen_card, player_card_deck, player_hp, enemy_card, enemy_card_deck, enemy_hp, turn)
    else:  # Defense
        print(f"\033[94m{enemy_card} is attacking!\033[0m")
        time.sleep(1)
        enemy_hp, player_hp, turn, enemy_card_is_not_summoned, player_card_is_not_summoned \
            = battle(enemy_card, enemy_card_deck, enemy_hp, chosen_card, player_card_deck, player_hp, turn)
    if enemy_hp <= 0 and player_hp <= 0:
        print("\033[91mMassacre with no winner!\033[0m")
        print(f"\033[91mGame Over!\033[0m")
        break
    elif enemy_hp <= 0:
        print("\033[93mWinner!\033[0m")
        print("\033[93mYou are the new Card Master!\033[0m")
        break
    elif player_hp <= 0:
        print("\033[91mYou have been killed.\033[0m")
        print(f"\033[91mGame Over!\033[0m")
        break
    turn += 1

# if card is destroyed - damages player hp by 200

# special_cards
# death_scythe - attack 550 / hp 500 / every attack drains enemy PLAYER hp by 100 and transfers it to cards health
# shrapnel_mine - attack 200 / hp 0 / attack ones and self destroys.
# if destroyed damages enemy card by 500 and enemy hp by 100
# the_trickster - attack 350 / hp 500  / attack ones, switch card and enemy player misses turn
# succubus - attack 300 / hp 470 / reduces enemy attack by 200 for current attack

# normal_cards
# dark_magician - attack 450 / hp 600
# high_elf - attack 400 / hp 490
# giant_tortoise - attack 250 / hp 700
# lizard_general - attack 390 / hp 500
# snowman - attack 300 / hp 450
# viking - attack 430 / hp 550
