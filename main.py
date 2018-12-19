import pygame
import display, cards
import functools, random, copy

pygame.init()

gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#gameDisplay = pygame.display.set_mode((1024,720))

pygame.display.set_caption("President")
w_screen = gameDisplay.get_size()[0]
h_screen = gameDisplay.get_size()[1]

w_img = int(500*341/w_screen)
h_img = int(726.0*240.0/h_screen)

cards.init_dimensions(gameDisplay)

clock = pygame.time.Clock()

hands = []
player_imgs = []
num_players = 8 #TODO fix

board = [] #list of tuples containing board cards
playing = None

cardback_img = pygame.image.load("cardback.png")
cardback_img = pygame.transform.smoothscale(cardback_img, (w_img,h_img))
gold_img = pygame.image.load("gold.png")
gold_img = pygame.transform.smoothscale(gold_img, (w_img, w_img))
silver_img = pygame.image.load("silver.png")
silver_img = pygame.transform.smoothscale(silver_img, (w_img, w_img))
arrow_img = pygame.image.load("arrow.png")
flag_img = pygame.image.load("flag.png")

start_deck = None
start_buttons = []
def load_start_buttons():
    w = w_screen /2
    h = h_screen /10
    def set_players(count):
        global num_players
        num_players = count
        load_start()
    for i in range(3,9):
        button = display.Button(str(i)+ " Players",(w_screen/2-w/2, i*(h+5)-50, w, h), (120,120,120))
        button.action = functools.partial(set_players, i)
        start_buttons.append(button)
    title = display.Text("President", (w_screen/2,h_screen/10,0,0),(255,255,255),80)
    start_buttons.append(title)

def load_start():
    global start_deck
    start_buttons.clear()
    start_deck = display.ImageButton(cardback_img, (w_screen/2-w_img/2,h_screen/2-h_img/2))
    def remove():
        global start_deck
        start_deck = None
    start_deck.actions.append(remove) #disappears after click
    start_deck.actions.append(start)
    
    print("loaded")

board_imgs = [] #only shows top tuple of board
opponent_imgs = []
    
def update_board_imgs():
    board_imgs.clear()
    if len(board)!=0:
        gap = 30
        total_width = len(board[-1])*gap+w_img
        x = w_screen/2-total_width/2
        for card in board[-1]:
            board_imgs.append(display.Image(card.img, (x,h_screen/2-h_img/2)))
            x+=gap

def update_opponent_imgs():
    opponent_imgs.clear()
    num_imgs = num_players - 1
    gap = 5
    x_start = w_screen/2 - num_imgs/2.0*w_img - (num_imgs - 1)/2.0*gap
    for img_count in range(num_imgs):
        hand = hands[img_count+1]
        if len(hand.cards) != 0:
            x = x_start+img_count*(gap+w_img)
            y = -h_screen/10
            img = display.Image(cardback_img, (x, y))
            if playing == img_count+1:
                arr_x = img.point[0] + img.get_dimension()[2]/2 - arrow_img.get_size()[0]/2
                arr_y = img.point[1] + img.get_dimension()[3] + 20
                arrow = display.Image(arrow_img, (arr_x, arr_y))
                opponent_imgs.append(arrow)
            if dominant == img_count+1:
                f_x = img.point[0] + img.get_dimension()[2]/2 - flag_img.get_size()[0]/2
                f_y = img.point[1] + img.get_dimension()[3] + 5
                flag = display.Image(flag_img, (f_x, f_y))
                opponent_imgs.append(flag)
            opponent_imgs.append(img)
            opponent_imgs.append(display.Text(str(len(hand.cards)),img.get_dimension(),(0,0,0)))
        elif hand.win == 1 or hand.win == 2:
            x = x_start+img_count*(gap+w_img)
            y = -h_screen/10+h_img - w_img
            if hand.win == 1:
                crown = display.Image(gold_img, (x, y))
            else:
                crown = display.Image(silver_img, (x, y))
            opponent_imgs.append(crown)

play_button = None
pass_button = None
first = True

selected_list = []
def update_player_imgs():
    global selected_list
    def bump(button,val):
        if button.bumped:
            button.dimension = (button.dimension[0],button.dimension[1]+50,button.dimension[2],button.dimension[3])
            selected_list.remove(val)
        else:
            button.dimension = (button.dimension[0],button.dimension[1]-50,button.dimension[2],button.dimension[3])
            selected_list.append(val)
        button.bumped = not button.bumped
        update_buttons()
    gap = 50
    hand_width = len(hands[0].cards)*gap+w_img
    x = w_screen/2 - hand_width/2
    for img in player_imgs:
        img.actions.clear()
    player_imgs.clear()
    for card in hands[0].cards:
        img_copy = copy.copy(card.img_button)
        img_copy.dimension =(x,h_screen*1.1-h_img, w_img, h_img)
        img_copy.actions.append(functools.partial(bump, img_copy, card))
        player_imgs.append(img_copy)
        x+=gap
    if hands[0].win == 1 or hands[0].win == 2:
        x = w_screen/2 - w_img/2
        y = h_screen - w_img
        if hand.win == 1:
            crown = display.Image(gold_img, (x, y))
        else:
            crown = display.Image(silver_img, (x, y))
        player_imgs.append(crown)

buttons = []
def update_buttons():
    global play_button, pass_button, board, first
    buttons.clear()
    
    if playing == 0:
        button_size = 74
        play_button = display.Button("PLAY",(w_screen-button_size, h_screen-button_size, button_size, button_size),(0,150,0))
        pass_button = display.Button("PASS",(0, h_screen-button_size, button_size, button_size),(255,0,0))
        play_button.action = functools.partial(receive_button, "play")
        pass_button.action = functools.partial(receive_button, "pass")

        #print("LIST")
        #for card in selected_list:
        #    print(card)
        #print("/LIST")
        play_button_status = True
        #determine if player can click "play"
        if len(selected_list) == 0:
            play_button_status = False
        elif len(board) == 0:
            rank = selected_list[0].rank
            has_toc = False
            toc = cards.Card(3, "C")
            for card in selected_list:
                if card.strictly_equals(toc):
                    has_toc = True
                if card.rank != rank:
                    play_button_status = False
                    break
            if first and not has_toc:
                play_button_status = False
        elif len(selected_list) != len(board[-1]):
            play_button_status = False
        else:
            rank = selected_list[0].rank
            for card in selected_list:
                if card < board[-1][0] or card.rank != rank:
                    play_button_status = False
                    break
        play_button.on = play_button_status

        arr_x = w_screen/2 - arrow_img.get_size()[0]/2
        arr_y = h_screen*1.1-h_img - 60 -arrow_img.get_size()[0]
        arrow = display.Image(arrow_img, (arr_x, arr_y))
        buttons.append(arrow)

        if first:
            pass_button.on = False
    
    elif playing != None:
        play_button = None
        pass_button = None

    if dominant == 0:
        f_x = w_screen/2 - flag_img.get_size()[0]/2
        f_y =  h_screen*1.1-h_img - 60 - flag_img.get_size()[1]
        flag = display.Image(flag_img, (f_x, f_y))
        buttons.append(flag)

def start(president = None):
    global playing
    if num_players != 0:
        for x in range(num_players):
            hands.append(cards.Deck())
    deck = cards.Deck()
    deck.fill()
    deck.shuffle()
    #deal cards
    if president == None:
        deal_to = random.randint(0,len(hands)-1)
    else:
        deal_to = president
    while len(deck.cards) > 0:
        hands[deal_to].push(deck.pop())
        deal_to += 1
        if deal_to >= len(hands):
            deal_to = 0
    for hand in hands:
        hand.cards.sort()

    #display player hand
    update_player_imgs()

    #display opponent decks
    update_opponent_imgs()

    #determine who goes first
    if president == None:
        three_of_clubs = cards.Card(3, "C")
        for hand in hands:
            if hand.has_card(three_of_clubs):
                playing = hands.index(hand)
                break
    else:
        playing = president

    print(playing)

    play()

dominant = None #player who is in control
def play():
    global playing, board, first, dominant
    place = 1
    game_over = False
    
    while not game_over:
        passed = False
        if dominant == playing:
            #clear
            print("CLEAR")
            board.clear()
            dominant = None
            update_board_imgs()
            game_loop(120, True)

        print(str(playing)+": ", end='')
        if len(hands[playing].cards) == 0:
            playing += 1
            if playing >= num_players:
                playing -= num_players
            print("DONE")
            update_opponent_imgs()
            update_buttons()
            continue
        elif playing == 0:
            passed = not prompt()
        else:
            passed = not play_card_from(hands[playing])
        if passed:
            print("PASS")
        else:
            dominant = playing
            if len(hands[playing].cards) == 0:
                hands[playing].win = place
                place += 1
        skip_count = skip()
        if skip_count != 4:
            if passed:
                playing+=1
            else:
                playing += skip_count
            if playing >= num_players:
                playing -= num_players
        if first:
            first = False
        update_buttons()
        update_player_imgs()
        update_opponent_imgs()
        game_loop(120, True)
        players_remaining = 0
        for hand in hands:
            if len(hand.cards) != 0:
                players_remaining += 1
        game_over = players_remaining <= 1

waiting_prompt = True
passed_prompt = None
def prompt():
    global waiting_prompt
    update_buttons()
    while waiting_prompt:
        game_loop(1, True)
    waiting_prompt = True
    return not passed_prompt

def receive_button(cmd):
    global waiting_prompt, passed_prompt
    if cmd == "play":
        for card in selected_list:
            print(str(card)+" ", end='')
        print()
        board.append(tuple(selected_list))
        for card in selected_list:
            hands[0].cards.remove(card)
        selected_list.clear()
        update_player_imgs()
        update_board_imgs()
        passed_prompt = False
    elif cmd == "pass":
        passed_prompt = True
    waiting_prompt = False

def skip(): #how many players skipped; if 4 then clear
    global board
    if len(board) == 0:
        return 1
    top_rank = board[-1][0].rank
    if top_rank == 2 or top_rank == 8:
        return 4
    tup_size = len(board[-1])
    connected_cards = []
    connected_tuples = []
    for tup in reversed(board):
        for card in tup:
            if card.rank == top_rank:
                connected_cards.append(card)
            else:
                break
        if tup[0].rank == top_rank:
            connected_tuples.append(tup)
        else:
            break
    if len(connected_cards) == 4:
        return 4
    return len(connected_tuples)

def play_card_from(hand):
    global board
    played = False
    play_list = []
    if len(board) == 0:
        for card in hand.cards:
            if len(play_list) == 0 or play_list[-1]==card:
                play_list.append(card)
            else:
                break
        played = True
    else:
        cards_count = len(board[-1])
        for card in hand.cards:
            if card >= board[-1][0] and (len(play_list) == 0 or play_list[-1]==card):
                play_list.append(card)
                if len(play_list) == cards_count:
                    break
        played = len(play_list) == cards_count
    if played:
        board.append(tuple(play_list))
        for card in play_list:
            hand.cards.remove(card)
            print(str(card)+" ", end='')
        print()
    update_board_imgs()
    return played #False if passed

def update(gameDisplay, event):
    for img in reversed(player_imgs): #images on top are prioritized
        img.update(gameDisplay, event)
    for img in start_buttons:
        img.update(gameDisplay,event)
    if start_deck != None:
        start_deck.update(gameDisplay, event)
    if play_button != None:
        play_button.update(gameDisplay,event)
    if pass_button != None:
        pass_button.update(gameDisplay,event)
def draw(gameDisplay):
    for img in player_imgs:
        img.draw(gameDisplay)
    for img in opponent_imgs:
        img.draw(gameDisplay)
    for img in board_imgs:
        img.draw(gameDisplay)
    if start_deck != None:
        start_deck.draw(gameDisplay)
    if play_button != None:
        play_button.draw(gameDisplay)
    if pass_button != None:
        pass_button.draw(gameDisplay)
    for img in start_buttons:
        img.draw(gameDisplay)
    for img in buttons:
        img.draw(gameDisplay)

game_exit = False
def game_loop(times = 1, override_quit = False, update_fn = update, draw_fn = draw):
    global game_exit
    for time in range(times):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                if override_quit:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                    if override_quit:
                        pygame.quit()
                        quit()
            update_fn(gameDisplay, event)
        
        gameDisplay.fill((0,0,0))
        draw_fn(gameDisplay)
        pygame.display.update()
        clock.tick(60)

load_start_buttons()

while not game_exit:
    game_loop()
pygame.quit()
quit()