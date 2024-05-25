export const loadGoogleMaps = (apiKey) => {
  return new Promise((resolve, reject) => {
    if (typeof google !== 'undefined') {
      resolve(google);
      return;
    }

    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}libraries=places&v=weekly&callback=vueGoogleMapsInit`;
    script.async = true;
    script.defer = true;
    script.onload = () => {
      resolve(google);
    };
    script.onerror = (error) => {
      reject(error);
    };

    document.head.appendChild(script);
  });
};
