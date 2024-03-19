import requests
import threading

# Fonction pour effectuer le brute forcing pour une partie du wordlist
def brute_force_partial(url, wordlist, start_index, end_index, results):
    with open(wordlist, 'r') as f:
        directories = f.readlines()[start_index:end_index]
    
    for directory in directories:
        directory = directory.strip()
        full_url = url + "/" + directory
        print("Testing:", full_url)  # Afficher le chemin testé
        response = requests.get(full_url)
        if response.status_code == 200:
            results.append(full_url)

# Fonction principale pour diviser le wordlist et démarrer les threads
def multi_threaded_brute_force(url, wordlist, num_threads):
    # Liste pour stocker les résultats trouvés
    results = []
    
    # Diviser le wordlist en fonction du nombre de threads
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        chunk_size = len(lines) // num_threads
        threads = []

        for i in range(num_threads):
            start_index = i * chunk_size
            end_index = start_index + chunk_size if i < num_threads - 1 else len(lines)
            thread = threading.Thread(target=brute_force_partial, args=(url, wordlist, start_index, end_index, results))
            threads.append(thread)
            thread.start()

        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()

    return results

# Utilisation de l'outil
url = "http://127.0.0.1:5000"
wordlist = "dir_list.txt"
num_threads = 3
found_paths = multi_threaded_brute_force(url, wordlist, num_threads)

# Afficher les chemins trouvés
print("Chemins trouvés :")
for path in found_paths:
    print(path)
