(() => {
  function xhttp(method, url, fn, data=null) {
    x = new XMLHttpRequest();
    
    x.onreadystatechange = fn;
    x.responseType = 'json';
    x.open(method, url);
    x.send();
  }

  ////
  // consonantChart
  //
  // When provided with a phonological inventory, the consonantChart class
  // generates a (Bootstrap-styled) HTML table with each of the consonants.
  var consonantChart = {
    props: {
      inventory: []
    },

    data: () => {
      return {
        places: [],
        manners: [],
        sounds: {}
      };
    },

    created() {
      // TODO: Generate places and manners from inventory
      //   - Modify server to provide places
      //   - Modify server to provide manners
      //   - Modify server to provide sounds with descriptions
      this.places = [
        'Bilabial',
        'Alveolar',
        'Velar'
      ];

      this.manners = [
        'Plosive',
        'Dental',
        'Fricative'
      ];

      // TODO: Generate sounds from inventory.
      this.sounds = {
        'voiceless-Bilabial-Plosive': 'p',
        'voiced-Bilabial-Plosive': 'b',
        'voiceless-Alveolar-Plosive': 't',
        'voiceless-Velar-Fricative': 'x'
      };
    },

    template: `
<table class="table">
  <thead>
    <tr>
      <th></th>
      <th v-for="place in places">
        {{place}}
      </th>
    </tr>
  </thead>

  <tbody>
    <tr v-for="manner in manners">
      <th>{{manner}}</th>
      <td v-for="place in places">
        <span class="text-left">{{sounds['voiceless-' + place + '-' + manner]}}</span>
        <span class="text-right">{{sounds['voiced-' + place + '-' + manner]}}</span>
      </th>
    </tr>
  </tbody>
</table>
`,
  };

  ////
  // app
  //
  // The primary Vue application.
  var app = new Vue({
    el: '#app',
     
    data: {
      instanceID: -1,
      inventory: [],

      query: ''
    },

    methods: {
      addConstraint: () => {
        console.log(app.query);
        // TODO: Submit POST request to server.
      }
    },

    components: {
      'consonant-chart': consonantChart
    },
    
    created() {
      var onLoad = {
        instanceID: {
          url: '/api/newinstance',
          method: 'POST'
        },

        inventory: {
          url: '/api/:instanceid/sounds',
          method: 'GET',
          data: {
            instanceid: () => { return app.instanceID; }
          }
        }
      }

      xhttp(
        'POST',
        '/api/newinstance',
        () => {
          if (x.readyState === XMLHttpRequest.DONE && x.status === 200)
          {
            app.instanceID = x.response.data;
          }
        }
      )
    }
  });
})();
