import requests
import json
import re

def clean_html(text):
    """移除 HTML 标签，用于 gear、weapon 和 mod 的属性"""
    if not text or text == '-':
        return '-'
    return re.sub(r'<[^>]+>', '', text).strip()

def fetch_gears_by_vendor(vendor_name):
    url = "https://rubenalamina.mx/division/gear.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        all_gears = resp.json()
    except Exception as e:
        print(f"抓取 gear.json 失败: {e}")
        return []

    result = []
    for gear in all_gears:
        if gear.get('vendor') != vendor_name:
            continue
        attrs_raw = gear.get('attributes', '')
        if '<br/>' in attrs_raw:
            parts = attrs_raw.split('<br/>')
            sec1 = clean_html(parts[0]) if parts else '-'
            sec2 = clean_html(parts[1]) if len(parts) > 1 else '-'
        else:
            sec1 = clean_html(attrs_raw) if attrs_raw else '-'
            sec2 = '-'

        item = {
            "name": gear.get('name', '-'),
            "brand": gear.get('brand', '-'),
            "type": gear.get('slot', '-'),
            "Core": clean_html(gear.get('core', '-')),
            "attribute1": sec1,
            "attribute2": sec2,
            "talent": clean_html(gear.get('talents', '-'))
        }
        result.append(item)
    return result

def fetch_weapons_by_vendor(vendor_name):
    url = "https://rubenalamina.mx/division/weapons.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        all_weapons = resp.json()
    except Exception as e:
        print(f"抓取 weapons.json 失败: {e}")
        return []

    result = []
    for weapon in all_weapons:
        if weapon.get('vendor') != vendor_name:
            continue
        item = {
            "name": weapon.get('name', '-'),
            "dmg": weapon.get('dmg', '-'),
            "rpm": weapon.get('rpm', '-'),
            "talent": weapon.get('talent', '-'),
            "attribute1": clean_html(weapon.get('attribute1', '-')),
            "attribute2": clean_html(weapon.get('attribute2', '-')),
            "attribute3": clean_html(weapon.get('attribute3', '-'))
        }
        result.append(item)
    return result

def fetch_mods_by_vendor(vendor_name):
    url = "https://rubenalamina.mx/division/mods.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        all_mods = resp.json()
    except Exception as e:
        print(f"抓取 mods.json 失败: {e}")
        return []

    result = []
    for mod in all_mods:
        if mod.get('vendor') != vendor_name:
            continue
        attrs_raw = mod.get('attributes', '')
        # 清理可能的 HTML 标签
        attrs_clean = clean_html(attrs_raw) if attrs_raw else ''
        if '<br/>' in attrs_raw:
            parts = attrs_raw.split('<br/>')
            type_part = clean_html(parts[0]) if parts else ''
            attr_part = clean_html(parts[1]) if len(parts) > 1 else ''
            type_val = type_part.lstrip() if type_part else '护甲模组'
            attr_val = attr_part.strip() if attr_part else '-'
        else:
            type_val = "护甲模组"
            attr_val = attrs_clean if attrs_clean else '-'
        item = {
            "name": mod.get('name', '-'),
            "type": type_val,
            "attributes": attr_val
        }
        result.append(item)
    return result

def fetch_all_vendors(keywords):
    all_data = {}
    for kw in keywords:
        gears = fetch_gears_by_vendor(kw)
        weapons = fetch_weapons_by_vendor(kw)
        mods = fetch_mods_by_vendor(kw)
        all_data[kw] = {
            "gears": gears,
            "weapons": weapons,
            "mods": mods
        }
    return all_data

if __name__ == "__main__":
    keywords = [
        'White House', 'Clan', 'The Theater', 'The Campus', 'The Castle',
        'DZ West', 'DZ South', 'DZ East', 'Haven', 'The Bridge', 'Cassie'
    ]
    data = fetch_all_vendors(keywords)
    with open("all_vendors.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("生成 all_vendors.json 完成")
