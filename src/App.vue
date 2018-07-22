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
            </div>
          </div>
      </div>
    </div>
    <div v-if="this.user != null && loading == true" class="row">
      <div class="col-sm-12">
          <img src="src/assets/loading.gif"/>
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
      loading: false
    };
  },
  firebase: function() {
    return {
      festivals: festivalsRef
    };
  },
  computed: {
    textFeature(){
      return this.fest == "" ? "a music festival" : this.fest;
    }
  },
  methods: {
    async login() {
      /**************
       *** AUTH *****
       **************
       this code is taken (very slightly modified) from https://glitch.com/edit/#!/spotify-implicit-grant?path=README.md:1:0
       which explains how to follow the spotify implicit grant authorization flow
      */
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
      const redirectUri = "http://localhost:8080/";
      const scopes = [
        "user-top-read user-read-private user-read-email"
      ];
      // If there is no token, redirect to Spotify authorization
      if (!this._token) {
        window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
          "%20"
        )}&response_type=token&show_dialog=true`;
      }
    }
  },
  created: function(){
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
      var retVal = false;
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
            retVal = true;
          },
          error => {
            console.log("error: " + error);
            retVal = false;
          }
        );
        return retVal;
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
.padded{
  margin-top: 0.75em;
}
.extra-padded{
  margin-top: 3em;
}
</style>
