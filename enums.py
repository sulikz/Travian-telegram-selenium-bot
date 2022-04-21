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


class Buildings(Enum):
    Town_Hall = 'Town Hall'
    Stonemasons_Lodge = 'Stonemason\'s Lodge'
    Treasury = 'Treasury'
    Wonder = 'Wonder of the World'
    Main_Building = 'Main Building'
    Cranny = 'Cranny'
    Palace = 'Palace'
    Residence = 'Residence'
    Marketplace = 'Marketplace'
    Trade_Office = 'Trade Office'
    Embassy = 'Embassy'
    Barracks = 'Barracks'
    Stable = 'Stable'
    Workshop = 'Workshop'
    Great_Barracks = 'Great Barracks'
    Great_Stable = 'Great Stable'
    Trapper = 'Trapper'
    City_Wall = 'City Wall'
    Earth_Wall = 'Earth Wall'
    Pallisade = 'Pallisade'
    Academy = 'Academy'
    Smithy = 'Smithy'
    Hero_Mansion = 'Hero\'s mansion'
    Rally_Point = 'Rally Point'
    Granary = 'Granary'
    Warehouse = 'Warehouse'
    Great_Granary = 'Great Granary'
    Great_Warehouse = 'Great Warehouse'
    Sawmill = 'Sawmill'
    Brickyard = 'Brickyard'
    Iron_foundry = 'Iron foundry'
    Grain_Mill = 'Grain Mill'
    Bakery = 'Bakery'


class AttackType(Enum):
    '''
    Attack type enum
    '''
    Normal = 'Attack: Normal'
    Raid = 'Attack: Raid'
    Reinforcement = 'Reinforcement'
