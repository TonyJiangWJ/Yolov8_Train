# 蚂蚁森林
ant_forest = {
    0: "cannot",
    1: "collect",
    2: "countdown",
    3: "help_revive",
    4: "item",
    5: "tree",
    6: "water",
    7: "waterBall",
    8: "stroll_btn",
    9: "sea_ball",
    10: "sea_garbage",
    11: "backpack",
    12: "gift",
    13: "magic_species",
    14: "one_key",
    15: "patrol_ball",
    16: "reward",
    17: "sea_ocr",
    18: "energy_ocr",
    19: "close_icon",
    20: "cooperation",
}
ant_forest_chz = {
    0: "cannot",
    1: "collect",
    2: "countdown",
    3: "help_revive",
    4: "item",
    5: "tree",
    6: "water",
    7: "waterBall",
    8: "stroll_btn",
    9: "sea_ball",
    10: "sea_garbage",
    11: "backpack",
    12: "gift",
    13: "magic_species",
    14: "one_key",
    15: "patrol_ball",
    16: "reward",
    17: "sea_ocr",
    18: "energy_ocr",
    19: "close_icon",
    20: "cooperation",
}
# 蚂蚁庄园
manor = {
    0: "booth_btn",
    1: "collect_coin",
    2: "collect_egg",
    3: "collect_food",
    4: "cook",
    5: "countdown",
    6: "donate",
    7: "eating_chicken",
    8: "employ",
    9: "empty_booth",
    10: "feed_btn",
    11: "friend_btn",
    12: "has_food",
    13: "has_shit",
    14: "hungry_chicken",
    15: "item",
    16: "kick-out",
    17: "no_food",
    18: "not_ready",
    19: "operation_booth",
    20: "plz-go",
    21: "punish_booth",
    22: "punish_btn",
    23: "signboard",
    24: "sleep",
    25: "speedup",
    26: "sports",
    27: "stopped_booth",
    28: "thief_chicken",
    29: "close_btn",
    30: "collect_muck",
    31: "confirm_btn",
    32: "working_chicken",
    33: "bring_back",
    34: "leave_msg",
    35: 'speedup_eating',
}

manor_chz = {
    0: "摆摊赚币",
    1: "收集金币",
    2: "收集蛋蛋",
    3: "领取饲料",
    4: "去做饭",
    5: "倒计时",
    6: "捐蛋",
    7: "吃饭鸡",
    8: "雇佣",
    9: "空摊位",
    10: "喂食按钮",
    11: "好友",
    12: "有饭",
    13: "有屎",
    14: "饿鸡",
    15: "道具",
    16: "赶走",
    17: "没饭",
    18: "蛋未完成",
    19: "可操作摊位",
    20: "请走",
    21: "可以贴罚单",
    22: "贴罚单",
    23: "公告牌",
    24: "去睡觉",
    25: "加速产豆",
    26: "去运动",
    27: "停产摊位",
    28: "小偷鸡",
    29: "关闭按钮",
    30: "收集饲料",
    31: "确认按钮",
    32: "工作鸡",
    33: "召回",
    34: "留言",
    35: '加速吃饭中'
}

yuanshen = {
    0: "button",
    1: "map",
    2: "paimeng",
    3: "person",
    4: "pet",
    5: "qiuqiu",
    6: "stone",
    7: "collect_stone",
    8: "entry_fire",
    9: "fire",
    10: "stone_tree",
    11: "wall",
    12: "wall_mark",
    13: "slime",
    14: "guardian",
}
yuanshen_chz = {
    0: "按钮",
    1: "地图",
    2: "派蒙",
    3: "角色",
    4: "漂浮宠物",
    5: "丘丘人",
    6: "矿石",
    7: "拾取矿石",
    8: "入口火柱",
    9: "墙壁火焰",
    10: "石化树",
    11: "石碑",
    12: "墙壁图腾",
    13: "史莱姆",
    14: "遗迹守卫"
}
tiktok = {
    0: "collect",
    1: "comment",
    2: "entry",
    3: "follow",
    4: "forward",
    5: "process_bar",
    6: "process_point",
    7: "zan",
    8: "ad_done",
    9: "ad_mark",
    10: "close_pop",
    11: "countdown",
    12: "finish_reward",
    13: "reward",
    14: "shop_countdown",
    15: "sign_confirm",
    16: "ad_loading",
    17: "chest",
    18: "loading_close",
}
# 星星球
manor_ball = {
    0: "ball",
    1: "chick",
    2: "boom",
}

manor_ball_chz = {
    0: "球",
    1: "小鸡",
    2: "炸弹",
}

# 遍历得到values，需要python3.8以上，否则顺序无法保证
def to_list(label_obj: dict):
    array_list = []
    for key in label_obj:
        array_list.append(label_obj[key])
    return array_list
