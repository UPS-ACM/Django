from django.core.management.base import BaseCommand, CommandError
from writing.models import Building, Bin, Floor
name = 'locations.csv'

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        curBuilding = ''
        curFloor = ''
        curLocation = ''

        class Bin:
            building = ''
            floor = ''
            location = ''
            binType = ''

            def __toString__(self):
                return self.building + ' ' + self.floor + ' ' + self.location + ' ' + self.binType

        Bins = []
        buildings = {}

        with open(name, 'r') as fin:
            for line in fin.readlines():
                if line.startswith("Building"):
                   continue
                   
                line = line.split(",")

                ###
                
                if line[0] != '':
                    curBuilding = line[0]
                    buildings[curBuilding] = {}

                if line[1] != '':
                    curFloor = line[1]
                    buildings[curBuilding] = curFloor

                # new location
                if line[2] != '':
                    curLocation = line[2]

                    b = Bin()
                    b.building = curBuilding
                    b.floor = curFloor
                    b.location = curLocation
                    b.binType = line[3]
                    Bins.append(b)
                        

                # Same location
                if line[3] != '' and line[2] == '':
                    b = Bin()
                    b.building = curBuilding
                    b.floor = curFloor
                    b.location = curLocation
                    b.binType = line[3]
                    Bins.append(b)

            # Make buildings and floors
            for build in buildings:
                b = Buiding(name = build)
                b.save()
                for x in buildings[build]:
                    f = Floor(name = x, building = Building.objects.get(name = build))
                    f.save()

            # Make bins
            for b in Bins:
                x = Bin(building = Building.objects.get(name = b.building),
                        description = b.binType, floor = Building.objects.get(name = b.floor),
                        location = b.location)
                x.save()
                
            for b in Bins:
                print b.__toString__()


