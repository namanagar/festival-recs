<template>
  <div id="app">
    <div class="row">
      <div class="col-sm-12">
        <h2>who2see</h2>
        <p>You're super excited to go to {{ textFeature }} - the headliners are sick. But who are you gonna watch earlier in the day 
          when the lineup is full of names you've never heard of? Your options are to listen to a ton of music (& not dig a lot of it) before the festival 
          to find the artists you do want to see, or just mill around on the day of. This app aims to help with that: we take your Spotify listening history,
          analyze it, and recommend sets to watch.
        </p>
      </div>
    </div>
   <div class="btn-group btn-group-lg btn-group-toggle" role="group" aria-label="festivals" v-for="festival in festivals" :key="festival.name">
     <label class="btn" :class="[(fest == festival) ? 'btn-success' : 'btn-outline-success']">
        <input type="radio" name="options" id="option1" autocomplete="off" :value="festival.name" v-model="fest"> {{ festival.name }}
      </label>
   </div>
  </div>
</template>

<script>
//import Preferences from "./assets/preferences";
//import axios to make the http requests to the spotify api
var spotify = require("spotify-web-api-js");
var firebase = require("firebase");
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
      fest: ""
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
  color: #f4f4f4;
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
</style>
