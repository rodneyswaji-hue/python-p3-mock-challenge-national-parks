# national_park_planner.py

# ------------------------
# NationalPark Class
# ------------------------
class NationalPark:
    _all_parks = []  # Keep track of all NationalPark instances

    def __init__(self, name):
        if not isinstance(name, str) or len(name) < 3:
            raise ValueError("NationalPark name must be a string of at least 3 characters")
        self._name = name
        self._trips = []  # trips to this park
        NationalPark._all_parks.append(self)

    @property
    def name(self):
        return self._name

    def trips(self):
        return self._trips

    def visitors(self):
        return list({trip.visitor for trip in self._trips})

    def total_visits(self):
        return len(self._trips)

    def best_visitor(self):
        if not self._trips:
            return None
        from collections import Counter
        visitors_count = Counter(trip.visitor for trip in self._trips)
        return visitors_count.most_common(1)[0][0]

    @classmethod
    def most_visited(cls):
        if not cls._all_parks:
            return None
        return max(cls._all_parks, key=lambda park: park.total_visits())


# ------------------------
# Visitor Class
# ------------------------
class Visitor:
    def __init__(self, name):
        if not isinstance(name, str) or not (1 <= len(name) <= 15):
            raise ValueError("Visitor name must be a string between 1 and 15 characters")
        self._name = name
        self._trips = []  # trips made by this visitor

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (1 <= len(value) <= 15):
            raise ValueError("Visitor name must be a string between 1 and 15 characters")
        self._name = value

    def trips(self):
        return self._trips

    def national_parks(self):
        return list({trip.national_park for trip in self._trips})

    def total_visits_at_park(self, park):
        return sum(1 for trip in self._trips if trip.national_park == park)


# ------------------------
# Trip Class
# ------------------------
class Trip:
    all = []  # Track all Trip instances

    def __init__(self, visitor, national_park, start_date, end_date):
        if not isinstance(visitor, Visitor):
            raise TypeError("visitor must be a Visitor instance")
        if not isinstance(national_park, NationalPark):
            raise TypeError("national_park must be a NationalPark instance")
        if not isinstance(start_date, str) or len(start_date) < 7:
            raise ValueError("start_date must be a string of at least 7 characters")
        if not isinstance(end_date, str) or len(end_date) < 7:
            raise ValueError("end_date must be a string of at least 7 characters")

        self._visitor = visitor
        self._national_park = national_park
        self._start_date = start_date
        self._end_date = end_date

        # Register trip with visitor and park
        visitor._trips.append(self)
        national_park._trips.append(self)

        # Register trip globally — THIS FIXES YOUR FAILING TEST
        Trip.all.append(self)

    @property
    def visitor(self):
        return self._visitor

    @property
    def national_park(self):
        return self._national_park

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if not isinstance(value, str) or len(value) < 7:
            raise ValueError("start_date must be a string of at least 7 characters")
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if not isinstance(value, str) or len(value) < 7:
            raise ValueError("end_date must be a string of at least 7 characters")
        self._end_date = value

if __name__ == "__main__":
    # Create visitors
    alex = Visitor("Alex")
    stacey = Visitor("Stacey")

    # Create parks
    yosemite = NationalPark("Yosemite")
    yellowstone = NationalPark("Yellowstone")

    # Create trips
    t1 = Trip(alex, yosemite, "September 1st", "September 5th")
    t2 = Trip(alex, yellowstone, "October 1st", "October 5th")
    t3 = Trip(alex, yosemite, "November 1st", "November 3rd")
    t4 = Trip(stacey, yosemite, "December 1st", "December 3rd")

    # Test methods
    print(alex.national_parks())                 # [Yosemite, Yellowstone]
    print(yosemite.visitors())                   # [Alex, Stacey]
    print(yosemite.total_visits())               # 3
    print(yosemite.best_visitor().name)          # Alex
    print(NationalPark.most_visited().name)      # Yosemite
    print(alex.total_visits_at_park(yosemite))   # 2