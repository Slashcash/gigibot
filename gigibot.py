import logging, random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def gigispread(update, context):
    spread(context.args[0].capitalize(), update, context)

def gigirandom(update, context):
    spread(pokemon_list[random.randint(0, len(pokemon_list)-1)], update, context)

def gigiadd(update, context):
    sentence = ""

    if len(context.args) < 2:
        update.message.reply_text('Ciao, il numero di parametri è insufficiente')
        return
    
    else:
        for i in range(1, len(context.args)):
            sentence += context.args[i] + " "

        #accounting for strange telegram behaviour
        sentence = sentence[:-1]

    if context.args[0] == "defense":
        additional_defensive_list.append(sentence)

        file = open("defensive_additional.txt", "a")
        file.write(sentence+"\n")
        file.close()
        update.message.reply_text('Ciao, aggiungerò questa frase a quelle sulla difesa')
    elif context.args[0] == "attack":
        additional_offensive_list.append(sentence)

        file = open("offensive_additional.txt", "a")
        file.write(sentence+"\n")
        file.close()
        update.message.reply_text('Ciao, aggiungerò questa frase a quelle offensive')
    elif context.args[0] == "speed":
        additional_speed_list.append(sentence)

        file = open("speed_additional.txt", "a")
        file.write(sentence+"\n")
        file.close()
        update.message.reply_text('Ciao, aggiungerò questa frase a quelle sulla speed')
    else:
        update.message.reply_text('Ciao, il comando è invalido non posso aggiungere la frase che desideri')

def spread(pokemon, update, context):
    if pokemon in pokemon_list:
        response = "Ciao, secondo me " + pokemon + " va giocato " + get_valid_spread() + ", "
        
        if first_stat == "Hp" or first_stat == "Def" or first_stat == "Sp. Def":
            response+="perché ti serve reggere " + move_list[random.randint(0, len(move_list)-1)] + \
            " di " + pokemon_list[random.randint(0, len(pokemon_list)-1)] \
            + " " + additional_defensive_list[random.randint(0, len(additional_defensive_list)-1)] 

        elif first_stat == "Atk" or first_stat == "Sp. Atk":
            response+="perché ti serve shottare " + pokemon_list[random.randint(0, len(pokemon_list)-1)] + \
            " " + additional_offensive_list[random.randint(0, len(additional_offensive_list)-1)]
        else:
            response+="perché ti serve outspeedare " + pokemon_list[random.randint(0, len(pokemon_list)-1)] + \
            " " + additional_speed_list[random.randint(0, len(additional_speed_list)-1)]

        update.message.reply_text(response)
    else:
        update.message.reply_text('Ciao, scusami ma qui ad Afragola questo Pokémon non è ancora arrivato!')


def get_valid_spread():
    #easter egg
    if random.randint(0, 4096) == 0:
        return "4 Hp / 252 Atk / 252 Spe"
    
    first_ev = random.randint(4, 252)
    while ((first_ev - 4)) % 8 != 0:
        first_ev+=1
	
    random_divider = random.randint(0, (508-first_ev)/2)
    while ((random_divider - 4)) % 8 != 0:
        random_divider+=1

    second_ev = int(((508-first_ev)/2)-random_divider)
    while first_ev + second_ev < 256:
            second_ev+=1	

    third_ev = 508 - first_ev - second_ev

    stats = ["Hp","Atk", "Def", "Sp. Atk", "Sp. Def", "Spe" ]
    global first_stat 
    first_stat = stats[random.randint(0, len(stats)-1)]

    second_stat = stats[random.randint(0, len(stats)-1)]
    while first_stat == second_stat:
        second_stat = stats[random.randint(0, len(stats)-1)]
                
    third_stat = stats[random.randint(0, len(stats)-1)]
    while first_stat == third_stat or second_stat == third_stat:
        third_stat = stats[random.randint(0, len(stats)-1)]    

    return str(first_ev) + " " + first_stat + " / " \
           + str(second_ev) + " " + second_stat + " / " \
           + str(third_ev) + " " + third_stat \
    

def main():
    print("Starting up bot...")

    #loading pokemon name files
    print("Loading pokemons...")
    pokemon_file = open("pokemon.txt", "r")

    global pokemon_list
    pokemon_list = []      

    for row in pokemon_file:
        pokemon_list.append(row[:-1])

    #loading pokemon moves
    print("Loading moves...")
    move_file = open("moves.txt", "r")
       
    global move_list
    move_list = []

    for row in move_file:
        move_list.append(row[:-1])

    #loading additional sentences for defensive spreads
    print("Loading additional sentences...")
    additional_defensive_file = open("defensive_additional.txt", "r")
       
    global additional_defensive_list
    additional_defensive_list = []

    for row in additional_defensive_file:
        additional_defensive_list.append(row[:-1])

    additional_defensive_file.close()

    #loading additional sentences for offensive spreads
    additional_offensive_file = open("offensive_additional.txt", "r")
       
    global additional_offensive_list
    additional_offensive_list = []

    for row in additional_offensive_file:
        additional_offensive_list.append(row[:-1])

    additional_offensive_file.close()

    #loading additional sentences for speed spreads
    additional_speed_file = open("speed_additional.txt", "r")
       
    global additional_speed_list
    additional_speed_list = []

    for row in additional_speed_file:
        additional_speed_list.append(row[:-1])

    additional_speed_file.close()

    #loading secret bot token
    token_file = open("token.txt", "r")
    updater = Updater(token_file.read().rstrip("\n"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("gigispread", gigispread))
    dp.add_handler(CommandHandler("gigirandom", gigirandom))
    dp.add_handler(CommandHandler("gigiadd", gigiadd))
    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
