import time
import json
import logging
from random import randint
from random import choice

with open("./json_data/items.json") as f:
	item_info = json.load(f)

# --------------------
# Static API responses
# --------------------

STATIC_GET_RESPONSES = {
    "pgl.news.information_list":   b'{"list":[], "total_count":0}',
    "pgl.member.profile.my_state": b"{}",
    "pgl.top.init":                b"{}",
    "pdw.home.my_island":          b'{"island_id":201, "arranged_interior_list":[]}',
    "pdw.home.my_bridge":          b"{}",
    "pdw.croft.tutorial_start":    b"{}",
    "pdw.croft.tutorial_end":      b"{}",
}

STATIC_POST_RESPONSES = {
    "pdw.home.pdw_timecheck":        b"{}",
    "pgl.member.profile.pdw_login":  b"{}",
}


# ---------------------
# Dynamic API responses
# ---------------------

def handle_my_croft_list(_query):
    croft_template = {
        "kinomi_state": 0,
        "my_croft_id":  0,
        "pokeitem_id":  0,
        "kinomi":       0,
        "kinomi_id":    52,
        "dirt_hp":      0,
    }
    response = {
        "croft_list": [
            {**croft_template, "x": 1, "y": 1},
            {**croft_template, "x": 2, "y": 1},
        ],
        "diglett_flag": 0,
    }
    return json.dumps(response).encode()


def handle_dreamland_top(_query):
    response = {
        "dreamland_area_id": randint(3, 9),
        "object_list": [],
    }
    return json.dumps(response).encode()


def handle_dreamland_tree_top(_query):
    count = randint(1, 10)
    pokemon_list = [
        {"pokemon_no": randint(0, 649), "form_no": 0}
        for _ in range(count)
    ]
    encount_list = [
        {
            **p,
            "pokename":        "TODO",
            "waza_name_disp":  "TODO",
            "speabi3":         "TODO",
        }
        for p in pokemon_list
    ]
    response = {"pokemon_list": pokemon_list, "encount_list": encount_list}
    logging.info("tree_top response: %s", json.dumps(response))
    return json.dumps(response).encode()

def handle_item_list(_query):
    item_list = []
    for _ in range(randint(1, 10)):
        item_id = choice(list(item_info.keys()))
        item_name = item_info.get(item_id, "TODO")["item_name"]
        item_list.append(
            {
                "pokeitem_id": int(item_id),
                "pokeitem": item_name,
                "item_cnt": str(randint(1, 99)),
                "bunrui_no": "1", #for sorting
                "b_hozon_sentou": "1", #for sorting
                "date": "2026-05-03"
            }
        )
    response = {"cnt": str(len(item_list)), "list": item_list}
    return json.dumps(response).encode()

def handle_pdw_start(_query):
    return json.dumps({"started_at": int(time.time())}).encode()


DYNAMIC_GET_RESPONSES = {
    "pdw.croft.my_croft_list":   handle_my_croft_list,
    "pdw.dreamland.top":         handle_dreamland_top,
    "pdw.dreamland.tree_top":    handle_dreamland_tree_top,
    "pdw.item.item_list":        handle_item_list
}

DYNAMIC_POST_RESPONSES = {
    "pdw.home.pdw_start": handle_pdw_start,
}