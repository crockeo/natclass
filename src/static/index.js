(() => {
  ////
  // app
  //
  // The primary Vue application.
  var app = new Vue({
    el: '#app',
     
    data: {
      loading: true,

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
          success: (response) => { self.updateInventory(); },
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
          (response) => { self.places = response.data; }
        );

        $.get(
          `/api/${self.instanceID}/manners`,
          (response) => { self.manners = response.data; }
        );

        $.get(
          `/api/${self.instanceID}/sounds`,
          (response) => {
            self.raw_sounds = response.data;
            for (var k in self.raw_sounds)
            {
              var prefix;
              if      (self.raw_sounds[k].voice === '+') prefix = 'voiced';
              else if (self.raw_sounds[k].voice === '-') prefix = 'voiceless';

              self.sounds[prefix + '-' + self.raw_sounds[k].place + '-' + self.raw_sounds[k].manner] = k;
            }

            self.loading = false
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
