import random
import art
batch1 = [2,3,4,5,6,7,8,9,10]
batch2 = ["Queen","King","Jack"]
as_card = ["As"]


def rnd_batch():
    batch = random.choice([batch1, batch2, as_card])
    return random.choice(batch)

def card_value(card, current_total=0, is_dealer=False):
    if card in batch2:
        return 10
    elif card in as_card:
        if is_dealer:
            return 11 if current_total + 11 <= 21 else 1
        else:
            ask1 = input("Do u want your as to be 1 or 11 ")
            return 11 if ask1.strip() == "11" else 1
    else:
        return card

def print_cards(cards, owner="Player"):
    print(f"{owner} cards:")
    for card in cards:
        art.art =art.card_art.get(card, "Card necunoscut")
        print(art.art)

def hit(total_value, cards):
    card = rnd_batch()
    cards.append(card)
    total_value += card_value(card, total_value, is_dealer=False)
    print(f"You drew: {card}")
    print(f"Your total is now: {total_value}")
    print_cards(cards, owner="Player")
    return total_value

def dealer_hit(total_value_dealer, dealer_cards):
    card = rnd_batch()
    dealer_cards.append(card)
    total_value_dealer += card_value(card, total_value_dealer, is_dealer=True)
    print(f"Dealer drew: {card}")
    print_cards(dealer_cards, owner="Dealer")
    print(f"Dealer total is now: {total_value_dealer}")
    return total_value_dealer

# Start joc

card1 = rnd_batch()
card2 = rnd_batch()
player_cards = [card1, card2]
player_value = card_value(card1, is_dealer=False) + card_value(card2, is_dealer=False)

dealer1 = rnd_batch()
dealer2 = rnd_batch()
dealer_cards = [dealer1, dealer2]
dealer_value = card_value(dealer1, is_dealer=True) + card_value(dealer2, is_dealer=True)

print_cards(player_cards, "Player")
print(f"Player total: {player_value}")
print(f"Dealer cards: [{dealer_cards[0]}, ?]")

while player_value < 21:
    choice = input("Hit or stand? ").lower()
    if choice == "hit":
        player_value = hit(player_value, player_cards)
    elif choice == "stand":
        break
    else:
        print("INVALID OPTION.")

while dealer_value < 17 :
    dealer_value = dealer_hit(dealer_value, dealer_cards)

print(f"Dealer's final hand:")
print_cards(dealer_cards, "Dealer")
print(f"Dealer total: {dealer_value}")

if dealer_value > 21:
    print("Dealer busts! Player wins!")
elif dealer_value > player_value:
    print("Dealer wins!")
elif dealer_value == player_value:
    print("It's a draw!")
else:
    print("Player wins!")
