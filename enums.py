from enum import Enum


class Troops(Enum):
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

    Phalanx = 'Phalanx'
    Swordsman = 'Swordsman'
    Pathfinder = 'Pathfinder'
    Theutates_Thunder = 'Theutates Thunder'
    Druidrider = 'Druidrider'
    Haeduan = 'Haeduan'
    Ram = 'Ram'
    Trebuchet = 'Trebuchet'
    Chieftain = 'Chieftain'

    Clubswinger = 'Clubswinger'
    Spearman = 'Spearman'
    Axeman = 'Axeman'
    Scout = 'Scout'
    Paladin = 'Paladin'
    Teutonic_Knight = 'Teutonic Knight'
    Catapult = 'Catapult'

    Settler = 'Settler'


class AttackType(Enum):
    '''
    Attack type enum
    '''
    Normal = 'Attack: Normal'
    Raid = 'Attack: Raid'
    Reinforcement = 'Reinforcement'
