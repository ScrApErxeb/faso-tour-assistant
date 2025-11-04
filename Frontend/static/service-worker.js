// Service Worker pour mode offline - Tourisme Burkina Faso PWA
const CACHE_NAME = 'tourisme-bf-v2.0';
const OFFLINE_URL = '/';

// Ressources à mettre en cache pour fonctionnement offline
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png',
  'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap',
  'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Flag_of_Burkina_Faso.svg/320px-Flag_of_Burkina_Faso.svg.png'
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installation en cours...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Mise en cache des ressources');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('[Service Worker] Installation réussie');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[Service Worker] Erreur installation:', error);
      })
  );
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activation...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[Service Worker] Activation réussie');
      return self.clients.claim();
    })
  );
});

// Interception des requêtes réseau
self.addEventListener('fetch', (event) => {
  // Stratégie: Network First, puis Cache
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la réponse est valide, la mettre en cache
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
        }
        
        return response;
      })
      .catch(() => {
        // Si le réseau échoue, chercher dans le cache
        return caches.match(event.request)
          .then((response) => {
            if (response) {
              console.log('[Service Worker] Réponse depuis le cache:', event.request.url);
              return response;
            }
            
            // Si pas dans le cache, retourner page offline
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});

// Synchronisation en arrière-plan (quand reconnexion)
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Synchronisation en arrière-plan');
  
  if (event.tag === 'sync-queries') {
    event.waitUntil(syncQueries());
  }
});

// Fonction de synchronisation des requêtes en attente
async function syncQueries() {
  console.log('[Service Worker] Synchronisation des requêtes...');
  
  // Récupérer les requêtes en attente depuis IndexedDB ou Cache
  const cache = await caches.open(CACHE_NAME);
  const requests = await cache.keys();
  
  // Renvoyer les requêtes
  const syncPromises = requests.map(async (request) => {
    try {
      const response = await fetch(request);
      if (response.ok) {
        await cache.put(request, response.clone());
        console.log('[Service Worker] Requête synchronisée:', request.url);
      }
    } catch (error) {
      console.error('[Service Worker] Erreur sync:', error);
    }
  });
  
  await Promise.all(syncPromises);
  console.log('[Service Worker] Synchronisation terminée');
}

// Gestion des notifications push (optionnel)
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Notification push reçue');
  
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle information disponible',
    icon: '/static/icon-192.png',
    badge: '/static/icon-192.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Découvrir',
        icon: '/static/icon-192.png'
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/static/icon-192.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Tourisme Burkina Faso', options)
  );
});

// Gestion des clics sur notifications
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] Notification cliquée:', event.action);
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

console.log('[Service Worker] Service Worker chargé et prêt');



