import matplotlib
import math
# Liste des villes fraçaises et de leurs coordonnées pour le traveling salesman problem
cities = {
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Toulouse": (43.6047, 1.4442),
    "Paris": (48.8566, 2.3522),
    "Nice": (43.7102, 7.2620)
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

def main():
    city1 = "Paris"
    city2 = "Lyon"
    city3 = "Marseille"
    city4 = "Toulouse"
    city5 = "Nice"
    print(calculate_distance(city2, city1))
    print(calculate_distance(city1, city4))
    print(calculate_distance(city4, city3))
    print(calculate_distance(city3, city5))
    print(calculate_distance(city5, city2))
    print("Bruteforce Traveling Salesman Problem Solution:")
    total_distance, path = bruteforce_travaling_salesman(cities)
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


if __name__ == "__main__":
    main()