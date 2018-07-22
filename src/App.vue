<template>
  <div id="app">
    <div class="row">
      <div class="col-sm-12">
        <h2><span style="color: #fb4f4f">who</span><span style="color: #6cc0e5">2</span><span style="color: #fbc93d">see</span></h2>
        <p>You're excited to see some of your favorite bands at {{ textFeature }}. But who are you gonna watch earlier in the day 
          when the lineup is full of names you've never heard of? Your options are to do a ton of research before the festival 
          to find the artists you do want to see, or just mill around on the day of. This app aims to help with that: we take your Spotify listening history,
          analyze it, and recommend sets to watch.
        </p>
      </div>
    </div>
    <div class="row padded">
      <div class="col-sm-12">
        <div class="btn-group btn-group-lg btn-group-toggle" role="group" aria-label="festivals" v-for="myFestival in festivals" :key="myFestival.name">
          <label class="btn" :class="[(fest == myFestival) ? 'btn-primary' : 'btn-outline-primary']">
            <input type="radio" name="options" id="option1" autocomplete="off" :value="myFestival.name" v-model="fest"> {{ myFestival.name }}
          </label>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
          <small class="center">Check back for more festivals - Gov Ball, Coachella, Bonnaroo, etc.!</small>
      </div>
    </div>
    <div  v-if="this.user == null" class="row extra-padded">
      <div class="col-sm-12">
          <button class="btn btn-lg btn-success" @click="login()"><i class="fab fa-spotify"/>  Log in with Spotify</button>
      </div>
    </div>
    <div v-if="this.user != null" class="row extra-padded">
      <div class="col-sm-12">
          <div class="card" style="width: 100%;">
            <div class="card-body">
              <h5 class="card-title">{{user.display_name}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{user.email}}</h6>
              <button class="btn btn-success" @click="generate()">Analyze!</button>
            </div>
          </div>
      </div>
    </div>
    <div v-if="this.user != null && loading == true" class="row">
      <div class="col-sm-12">
          <img src="src/assets/loading.gif"/>
      </div>
    </div>
    <div v-if="this.user != null && loading == false && guarantees.length > 0">
      <div class="row extra-padded">
        <div class="col-sm-12">
          <h4>Your Must Sees:</h4>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-4" v-for="artist in guarantees" :key="artist.artist">
          <div class="card" style="width: 100%;">
            <div class="card-body">
              <h5 class="card-title">{{artist.artist}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ formatStartDate(artist.startTime)}} - {{formatEndDate(artist.endTime)}}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
     <div v-if="this.user != null && loading == false && recommendations.length > 0">
      <div class="row extra-padded">
        <div class="col-sm-12">
          <h4>Recommendations:</h4>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-4" v-for="artist in recommendations" :key="artist.name">
          <div class="card" style="width: 100%;">
            <div class="card-body">
              <h5 class="card-title">{{artist.name}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ formatStartDate(artist.startTime)}} - {{formatEndDate(artist.endTime)}}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import Preferences from "./assets/preferences";
//import axios to make the http requests to the spotify api
var spotify = require("spotify-web-api-js");
var firebase = require("firebase");
var axios = require("axios");
// Initialize Firebase
var config = {
  apiKey: "AIzaSyCDvQPlAs_uSfVwNHdA27WwJeIFHN2rXIY",
  authDomain: "festival-recs.firebaseapp.com",
  databaseURL: "https://festival-recs.firebaseio.com",
  projectId: "festival-recs",
  storageBucket: "festival-recs.appspot.com",
  messagingSenderId: "215782282092"
};
var db = firebase.initializeApp(config).database();
var festivalsRef = db.ref("festivals");
export default {
  name: "app",
  data() {
    return {
      fest: "Lollapalooza 2018",
      _token: "",
      user: null,
      loading: false,
      topArtists: [],
      guarantees: [],
      relatedArtists: [],
      freqMap: [],
      recommendations: []
    };
  },
  firebase: {
    festivals: festivalsRef
  },
  computed: {
    textFeature() {
      return this.fest == "" ? "a music festival" : this.fest;
    }
  },
  methods: {
    formatStartDate(date) {
      var obj = new Date(date);
      //console.log(obj)
      //obj.setTime( obj.getTime() - new Date().getTimezoneOffset()*60*1000 );
      //console.log(obj)
      return (
        obj.toDateString().substring(0, 3) +
        " " +
        (obj.toLocaleTimeString("en-US").length < 11
          ? obj.toLocaleTimeString("en-US").substring(0, 4)
          : obj.toLocaleTimeString("en-US").substring(0, 5))
      );
    },
    formatEndDate(date) {
      var obj = new Date(date);
      //obj.setTime( obj.getTime() + new Date().getTimezoneOffset()*60*1000 );
      return obj.toLocaleTimeString("en-US").length < 11
        ? obj.toLocaleTimeString("en-US").substring(0, 4)
        : obj.toLocaleTimeString("en-US").substring(0, 5);
    },
    async login() {
      /* this code is taken (very slightly modified) from https://glitch.com/edit/#!/spotify-implicit-grant?path=README.md:1:0
       which explains how to follow the spotify implicit grant authorization flow */
      const hash = window.location.hash
        .substring(1)
        .split("&")
        .reduce(function(initial, item) {
          if (item) {
            var parts = item.split("=");
            initial[parts[0]] = decodeURIComponent(parts[1]);
          }
          return initial;
        }, {});
      //window.location.hash = "";
      // Set token
      this._token = hash.access_token;
      const authEndpoint = "https://accounts.spotify.com/authorize";
      // Replace with your app's client ID, redirect URI and desired scopes
      const clientId = "47d9e6f3d4364d13bc1a0572ed81a078";
      const redirectUri = "https://namanagar.github.io/festival-recs/"; //  http://localhost:8080/
      const scopes = ["user-top-read user-read-private user-read-email"];
      // If there is no token, redirect to Spotify authorization
      if (!this._token) {
        window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
          "%20"
        )}&response_type=token&show_dialog=true`;
      }
    },
    async getTopArtists() {
      await axios
        .get(`https://api.spotify.com/v1/me/top/artists?limit=50`, {
          headers: {
            Authorization: "Bearer " + this._token
          }
        })
        .then(
          response => {
            response.data.items.forEach(element => {
              this.topArtists.push({ id: element.id, name: element.name });
            });
          },
          error => {
            console.log("error: " + error);
          }
        );
    },
    findGuarantees() {
      var myFest = this.fest;
      var lineup = "";
      this.festivals.forEach(fest => {
        if (fest.name == myFest) {
          lineup = fest.lineup;
        }
      });
      var artistNames = this.topArtists.map(el => el.name);
      var matches = lineup.filter(artist => {
        return artistNames.includes(artist.artist);
      });
      return matches;
    },
    async getRelatedArtists(topArtists) {
      var artistIDs = topArtists.map(el => el.id);
      for (var i = 0; i < artistIDs.length; i++) {
        await axios
          .get(
            `https://api.spotify.com/v1/artists/${
              artistIDs[i]
            }/related-artists`,
            {
              headers: {
                Authorization: "Bearer " + this._token
              }
            }
          )
          .then(
            response => {
              //console.log(response.data);
              response.data.artists.forEach(element => {
                this.relatedArtists.push(element.name);
              });
            },
            error => {
              console.log("error: " + error);
            }
          );
      }
      return this.relatedArtists;
    },
    buildMap() {
      var myFest = this.fest;
      var lineup = "";
      this.festivals.forEach(fest => {
        if (fest.name == myFest) {
          lineup = fest.lineup;
        }
      });
      var lineupArtists = lineup.map(el => el.artist.toUpperCase());
      var guarantees = this.guarantees.map(el => el.artist.toUpperCase());
      this.relatedArtists.forEach(rel => {
        if (lineupArtists.includes(rel.toUpperCase()) && !guarantees.includes(rel.toUpperCase())) {
          var justNames = this.freqMap.map(el => el.name.toUpperCase())
          if (!justNames.includes(rel.toUpperCase())) {
            var obj = lineup.find(p => p.artist.toUpperCase() == rel.toUpperCase())
            this.freqMap.push({name: rel, count: 1, startTime: obj.startTime, endTime: obj.endTime});
          }
          else {
            let artist = this.freqMap.find(p => p.name == rel)
            artist.count += 1;
          }
        }
      });
      var byCount = this.freqMap.slice(0);
      byCount.sort(function(a,b) { return a.count - b.count; });
      this.recommendations = byCount;
    },
    async generate() {
      this.loading = true;
      await this.getTopArtists();
      this.guarantees = this.findGuarantees();
      await this.getRelatedArtists(this.topArtists);
      this.buildMap();
      this.loading = false;
    }
  },
  created: function() {
    const hash = window.location.hash
      .substring(1)
      .split("&")
      .reduce(function(initial, item) {
        if (item) {
          var parts = item.split("=");
          initial[parts[0]] = decodeURIComponent(parts[1]);
        }
        return initial;
      }, {});
    this._token = hash.access_token;
    const idk = hash.access_token;
    axios
      .get("https://api.spotify.com/v1/me", {
        headers: {
          Authorization: "Bearer " + this._token
        }
      })
      .then(
        response => {
          this.user = response.data;
          this._token = idk;
        },
        error => {
          console.log("error: " + error);
        }
      );
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Montserrat|Signika");
#app {
  font-family: "Montserrat", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2d2d2d;
  margin-left: 7.5vmax;
  margin-right: 7.5vmax;
  margin-top: 5vmax;
  margin-bottom: 5vmax;
}
h1,
h2 {
  font-weight: normal;
  font-family: "Signika";
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.fest-button {
  margin: 1em;
}
.center {
  text-align: center;
}
.padded {
  margin-top: 0.75em;
}
.extra-padded {
  margin-top: 3em;
}
</style>
