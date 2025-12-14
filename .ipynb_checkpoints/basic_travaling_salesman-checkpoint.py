import math
import time
import matplotlib.pyplot as plt
from carbontracker.tracker import CarbonTracker
# Liste des villes fraçaises et de leurs coordonnées pour le traveling salesman problem

NOMBRE_VILLE = 11

cities = {
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Toulouse": (43.6047, 1.4442),
    "Paris": (48.8566, 2.3522),
    "Nice": (43.7102, 7.2620),
    "Bordeaux": (44.8378, 2.0),
    "Nantes": (47.2184, 2.0),
    "Strasbourg": (48.5734, 7.7521),
    "Lille": (50.6292, 3.0573),
    "Rennes": (48.1173, 2.0),
    "Reims": (49.2583, 4.0317),
    "Le Havre": (49.4944, 0.1079),
    "Saint-Étienne": (45.4397, 4.3872),
    "Toulon": (43.1242, 5.9280),
    "Grenoble": (45.1885, 5.7245),
    "Dijon": (47.3220, 5.0415),
    "Angers": (47.4784, 3),
    "Nîmes": (43.8367, 4.3601),
    "Villeurbanne": (45.7719, 4.8902),
    "Clermont-Ferrand": (45.7772, 3.0870)
}

long_cities_list = {
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Toulouse": (43.6047, 1.4442),
    "Paris": (48.8566, 2.3522),
    "Nice": (43.7102, 7.2620),
    

}

def get_city_coordinates(city_name):
    """Retourne les coordonnées (latitude, longitude) d'une ville donnée."""
    return cities.get(city_name, None)

def calculate_distance(city1, city2):
    coords1 = get_city_coordinates(city1)
    coords2 = get_city_coordinates(city2)
    
    # Convert latitude and longitude to radians
    lat1 = math.radians(coords1[0])
    lon1 = math.radians(coords1[1])
    lat2 = math.radians(coords2[0])
    lon2 = math.radians(coords2[1])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    # Calculate the result
    return c * r

def bruteforce_travaling_salesman(cities_dict, start_city=None):
    remaining_cities = list(cities_dict.keys())
    
    # If this is the first call (not recursive), try each city as starting point
    if start_city is None:
        best_total = float('inf')
        best_path = []
        
        for city in remaining_cities:
            # Try this city as the starting point
            others_dict = {k: v for k, v in cities_dict.items() if k != city}
            distance, path = bruteforce_travaling_salesman(others_dict, city)
            if distance < best_total:
                best_total = distance
                best_path = [city] + path
        return best_total, best_path
    
    # Base case: if no cities left to visit
    if not remaining_cities:
        # Return to start city
        return calculate_distance(start_city, start_city), []
    
    # Try each remaining city as the next destination
    min_distance = float('inf')
    best_path = []
    
    for next_city in remaining_cities:
        # Calculate distance to this city
        current_distance = calculate_distance(start_city, next_city)
        
        # Recursively solve for remaining cities
        others_dict = {k: v for k, v in cities_dict.items() if k != next_city}
        sub_distance, sub_path = bruteforce_travaling_salesman(others_dict, next_city)
        
        total_distance = current_distance + sub_distance
        if total_distance < min_distance:
            min_distance = total_distance
            best_path = [next_city] + sub_path
            
    return min_distance, best_path


def debug_traveling_salesman(number_cities, cities):
    print("---------------------------------------------------------------------")
    print("Bruteforce Traveling Salesman Problem Solution for {number_cities}:")
    start_time = time.time()
    cuted_cities_list= dict(list(cities.items())[:number_cities])
    total_distance, path = bruteforce_travaling_salesman(cuted_cities_list)
    print("Individual distances along the path:")
    total = 0
    for i in range(len(path)):
        dist = calculate_distance(path[i], path[(i + 1) % len(path)])
        total += dist
        print(f"From {path[i]} to {path[(i + 1) % len(path)]}: {dist:.2f} km")
    
    print("\nBruteforce Traveling Salesman Problem Solution:")
    print(f"Total distance: {total:.2f} km")
    print(f"Path: {path}")
    print(f"Returns to {path[0]}")
    print("The execution took %s seconds ---" % (time.time() - start_time))


def main():
    # iterate adding one more city at each step and measure time per iteration
    max_iter = min(NOMBRE_VILLE, len(cities))
    ns = []
    times_ms = []
    tracker = CarbonTracker(1)
    tracker.epoch_start()
    for i in range(max_iter):
        n = i + 1
        ns.append(n)
        t0 = time.perf_counter()
        debug_traveling_salesman(n, cities)
        elapsed = (time.perf_counter() - t0)
        times_ms.append(elapsed)
    tracker.epoch_end()   

    # Plot timings
    try:
        plt.figure(figsize=(8, 5))
        plt.plot(ns, times_ms, marker='o')
        plt.xlabel('Number of cities')
        plt.ylabel('Time per iteration (s)')
        plt.title('TSP bruteforce: execution time vs number of cities')
        plt.grid(True)
        plt.savefig('timings.png')
        print('Saved timing plot to timings.png')
    except Exception as e:
        print('Could not plot timings:', e)
   

"""     # Long cities list
    total_distance, path = bruteforce_travaling_salesman(long_cities_list)
    print("Individual distances along the path:")
    total = 0
    for i in range(len(path)):
        dist = calculate_distance(path[i], path[(i + 1) % len(path)])
        total += dist
        print(f"From {path[i]} to {path[(i + 1) % len(path)]}: {dist:.2f} km")
    
    print("\nBruteforce Traveling Salesman Problem Solution:")
    print(f"Total distance: {total:.2f} km")
    print(f"Path: {path}")
    print(f"Returns to {path[0]}") """


if __name__ == "__main__":
    main()