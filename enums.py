from enum import Enum


class Roman(Enum):
    """
    Roman troops enum
    """
    Legionnaire = 'Legionnaire'
    Praetorian = 'Praetorian'
    Imperian = 'Imperian'
    Equites_Legati = 'Equites Legati'
    Equites_Imperiatoris = 'Equites Imperatoris'
    Equites_Caesaris = 'Equites Caesaris'
    Battering_Ram = 'Battering Ram'
    Fire_Catapult = 'Fire_Catapult'
    Senator = 'Senator'
    Settler = 'Settler'


class Gaul(Enum):
    """
    Gaul troops enum
    """
    Phalanx = 'Phalanx'
    Swordsman = 'Swordsman'
    Pathfinder = 'Pathfinder'
    Theutates_Thunder = 'Theutates Thunder'
    Druidrider = 'Druidrider'
    Haeduan = 'Haeduan'
    Ram = 'Ram'
    Trebuchet = 'Trebuchet'
    Chieftain = 'Chieftain'
    Settler = 'Settler'


class Teutons(Enum):
    """
    Teuton troops enum
    """
    Clubswinger = 'Clubswinger'
    Spearman = 'Spearman'
    Axeman = 'Axeman'
    Scout = 'Scout'
    Paladin = 'Paladin'
    Teutonic_Knight = 'Teutonic Knight'
    Ram = 'Ram'
    Catapult = 'Catapult'
    Chief = 'Chief'
    Settler = 'Settler'


class AttackType(Enum):
    '''
    Attack type enum
    '''
    Normal = 'Attack: Normal'
    Raid = 'Attack: Raid'
    Reinforcements = 'Reinforcement'
