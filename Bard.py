import log, copy

def combat(level: int, item1: str, item2: str, item3: str, astro: bool, chrono: int, sorcs: int, end: float, verbose=False):
    #determine initial stats
    base_as = .7
    as_mod = 1.0
    base_ap = 0
    mana = 0
    max_mana = 90
    cast_time = 1.5
    #special effects
    blue = False
    shojins = 0
    rabadons = 0
    guinsoos = 0
    rods = 0
    bows = 0
    tears = 0
    chalices = 0
    chrono_int = 0
    chrono_ticks = 0
    #apply items
    equipped = [item1, item2, item3]
    for i in equipped:
        if i == "tear":
            tears += 1
        elif i == "rod":
            rods += 1
        elif i == "bow":
            bows += 1
        elif i == "blue":
            tears += 2
            blue = True
        elif i == "shojin":
            tears += 1
            shojins += 1
        elif i == "ludens":
            tears += 1
            rods += 1
        elif i == "shiv":
            tears += 1
            bows += 1
        elif i == "chalice":
            tears += 1
            chalices += 1
        elif i == "guinsoos":
            bows += 1
            rods += 1
            guinsoos += 1
        elif i == "rabadons":
            rods += 2
            rabadons += 1
        elif i == "rapidfire":
            bows += 2
    mana += tears * 15
    as_mod += bows * .15
    base_ap += rods * .2
    #apply traits
    if astro:
        max_mana -= 30
    if sorcs >= 6:
        base_ap += .75
    elif sorcs >= 4:
        base_ap += .4
    elif sorcs >= .2:
        base_ap += .2
    if chrono >= 8:
        chrono_int = .75
    elif chrono >= 6:
        chrono_int = 1.5
    elif chrono >= 4:
        chrono_int = 3.5
    elif chrono >= 2:
        chrono_int = 8
    #apply level, rabadons, calculate mana generated
    if level == 1:
        base_mana_gen = 8
    elif level == 2:
        base_mana_gen = 20
    elif level == 3:
        base_mana_gen = 90
    
    #starting the loop
    time = 0
    meeps = 0
    if verbose: log.out("Starting Mana: " + str(int(mana)) + "/" + str(max_mana))
    while time < end:
        if mana >= max_mana:
            time += cast_time
            meeps += 1
            if blue:
                mana = 20
            else:
                mana = 0
            if verbose: log.out("Made a Meep at: " + str(round(time, 2)))
            continue
        while chrono >= 2 and time / chrono_int >= chrono_ticks:
            as_mod += .15
            chrono_ticks += 1
        aa_time = 1 / (base_as * as_mod)
        if aa_time < .2: aa_time = .2
        ap = base_ap
        if time < 10:
            ap = base_ap + .3 * chalices
        mana_gen = 10 + base_mana_gen * (1 + (ap + ap * .5 * rabadons))
        if meeps >= 1:
            mana_gen += shojins * .18 * max_mana
        time += aa_time
        mana = mana + mana_gen
        as_mod += .05 * guinsoos
        if verbose: log.out("Finished an aa at: " + str(round(time, 2)) + " and generated " + str(mana_gen) + " mana")
        if verbose: log.out("Current Mana: " + str(int(mana)) + "/" + str(max_mana) + " Meeps: " + str(meeps))
    return round(time / meeps, 3)

def create_text_file():
    items1 = ["empty", "bow", "rod", "tear", \
        "blue", "shojin", "ludens", \
        "shiv", "chalice", "guinsoos", \
        "rabadons", "rapidfire"]
    items2 = copy.copy(items1)
    items3 = copy.copy(items1)
    finished_items = []

    for item1 in items1:
        for item2 in items2:
            for item3 in items3:
                for level in [1, 2, 3]:
                    for astro in [False, True]:
                        for chrono in [0, 2, 4, 6, 8]:
                            for sorcs in [0, 2, 4, 6]:
                                for end in [10, 20, 30]:
                                    score = combat(level, item1, item2, item3, astro, chrono, sorcs, end)
                                    params = [str(score), str(level), item1, item2, item3, str(astro), str(chrono), str(sorcs), str(end)]
                                    separator = ","
                                    log.out(separator.join(params))
                                    log.file(separator.join(params), "bard_scores.txt")
            items3.remove(item2)
        finished_items.append(item1)
        items2 = copy.copy(items1)
        items3 = copy.copy(items1)
        for f in finished_items:
            items2.remove(f)
            items3.remove(f)
    return

def detailed_sim():
    level = 1
    item1 = "empty"
    item2 = "chalice"
    item3 = "chalice"
    astro = False
    chrono = 0
    sorcs = 2
    end = 30
    verbose = True
    score = combat(level, item1, item2, item3, astro, chrono, sorcs, end, verbose)
    params = [str(score), str(level), item1, item2, item3, str(astro), str(chrono), str(sorcs), str(end)]
    separator = ","
    log.out(separator.join(params))
    return

def list_combination_test():
    aa = ["0", "1" , "2"]
    bb = copy.copy(aa)
    cc = copy.copy(aa)
    fin = []

    for a in aa:
        for b in bb:
            for c in cc:
                log.out(a+b+c)
            cc.remove(b)
        fin.append(a)
        bb = copy.copy(aa)
        cc = copy.copy(aa)
        for f in fin:
            bb.remove(f)
            cc.remove(f)
    return

#list_combination_test()
#create_text_file()
detailed_sim()