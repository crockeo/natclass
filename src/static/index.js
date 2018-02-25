(() => {
  ////
  // placeOrder
  //
  // The the intended display order of the places received from the server.
  placeOrder = {
    'Bilabial': 0,
    'Labiodental': 1,
    'Dental': 2,
    'Alveolar': 3,
    'Postalveolar': 4,
    'Retroflex': 5,
    'Alveolopalatal': 6,
    'Palatal': 7,
    'Velar': 8,
    'Uvular': 9,
    'Pharyngeal': 10,
    'Glottal': 11
  };

  ////
  // mannerOrder
  //
  // The intended display order of the manners received from the server.
  mannerOrder = {
    'Plosive': 0,
    'Affricate': 1,
    'Fricative': 2,
    'Lateral Fricative': 3,
    'Nasal': 4,
    'Trill': 5,
    'Tap': 6,
    'Approximant': 7,
    'Lateral Approximant': 8,
    'Glide': 9
  };

  ////
  // app
  //
  // The primary Vue application.
  var app = new Vue({
    el: '#app',
     
    data: {
      places_loading: true,
      manners_loading: true,
      sounds_loading: true,

      instanceID: -1,

      sounds_raw: {},
      sounds: {},

      places: [],
      manners: [],

      query: ''
    },

    methods: {
      addConstraint() {
        var self = this;

        $.ajax(`/api/${self.instanceID}/constraint`, {
          contentType: 'application/json',
          data: JSON.stringify({ constraint: self.query }),
          success: (response) => {
            self.query = '';
            self.updateInventory();
          },
          type: 'POST'
        });
      },
      
      clearConstraints() {
        var self = this;
        $.post(
          `/api/${self.instanceID}/clear`,
          (response) => self.updateInventory()
        );
      },

      updateInventory() {
        var self = this;

        $.get(
          `/api/${self.instanceID}/places`,
          (response) => {
            self.places = response.data;
            self.places.sort((a, b) => {
              return placeOrder[a] - placeOrder[b];
            });

            self.places_loading = false;
          }
        );

        $.get(
          `/api/${self.instanceID}/manners`,
          (response) => {
            self.manners = response.data;
            self.manners.sort((a, b) => {
              return mannerOrder[a] - mannerOrder[b];
            });

            self.manners_loading = false
          }
        );

        $.get(
          `/api/${self.instanceID}/sounds`,
          (response) => {
            self.raw_sounds = response.data;
            self.sounds = {};

            for (var k in self.raw_sounds)
            {
              var prefix;
              if      (self.raw_sounds[k].voice === '+') prefix = 'voiced';
              else if (self.raw_sounds[k].voice === '-') prefix = 'voiceless';

              var key = prefix + '-' + self.raw_sounds[k].place + '-' + self.raw_sounds[k].manner;
              if (self.sounds[key] === undefined)
                self.sounds[key] = [];
              self.sounds[key].push(k);
            }

            self.sounds_loading = false
          }
        );
      }
    },
    
    created() {
      var self = this;

      $.post(
        '/api/newinstance',
        (response) => {
          self.instanceID = response.data;
          self.updateInventory();
        }
      );
    }
  });
})();
