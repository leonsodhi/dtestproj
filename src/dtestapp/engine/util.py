from dtestapp.models.item import Item

def getItem(itemName):
        #TODO: this should never fail but still prob want to check if item exists first, also, should have an identifier for the item rather than using the name
        return Item.objects.get(name__iexact=itemName)

def stricmp(s1, s2):
    return s1.lower() == s2.lower()
