<template>
</template>
  
<script setup>
import axios from 'axios';
import { ref } from 'vue';
let nums = ref();
let sta = ref([0, 0, 0]);
axios.get('http://localhost:8000/api/sta1/')
  .then(res => {
    nums.value = res.data.a;
    sta.value[0] = res.data.b;
    sta.value[1] = res.data.c;
    sta.value[2] = res.data.d;
  });
</script>
  
<style scoped>
#main {
  position: relative;
  top: 5%;
  height: 90%;
  display: flex;
  box-shadow: 0 0 5px rgb(57, 167, 176),
    0 0 10px rgb(56, 183, 145);
}

#left {
  flex: 1;
  background-image: linear-gradient(rgba(63, 126, 149, .9), rgba(85, 32, 159, .9));
  box-shadow: 0 0 10px rgb(85, 32, 159);
  z-index: 2;
}

#left li {
  margin: 5%;
  font-size: 25px;
  text-align: center;
  border-radius: 5px;
  list-style: none;
}

li#selected {
  background-color: rgba(0, 0, 0, .2);
}

#right {
  flex: 7;
  background-color: rgba(255, 255, 255, .9);
  z-index: 1;
}

#top {
  background-color: rgba(0, 0, 0, .1);
  box-shadow: 0 5px 10px #888;
}

#top li {
  margin: 1%;
  float: left;
  list-style: none;
}

#container {
  padding: 1%;
  height: 80%;
}

#icon {
  display: flex;
}
#header1 {
  margin: 0 3%;
  flex: 1;
  color: #4f4f4f;
  font-size: 35px;
  font-weight: bolder;
  border-radius: 1px;
  border-left: 5px solid #17a2b8;
  background-color: rgba(100,100,100,0.2);
}
#header2 {
  flex: 1;
  color: #4f4f4f;
  font-size: 30px;
  font-weight: bolder;
}

#list {
  width: 100%;
  height: 80%;
  overflow-y: scroll;
}

#pie {
  width: 100%;
  height: 100%;
}

h1 {
  font-size: 40px;
  color: #4f4f4f;
}

table {
  width: 95%;
  margin: auto;
  border-spacing: 0;
  border-collapse: collapse;
}

th {
  padding: 1% 0;
  background-color: #343a40;
  color: white;
}

td {
  padding: 1% 0;
  border: #aaa .5px solid;
  text-align: center;
}

a {
  color: white;
  text-decoration: none;
  transition: all 0.2s;
}

a:hover {
  color: #17a2b8;
  transition: all 0.2s;
}

div::-webkit-scrollbar {
  width: 10px;
}

div::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.4);
  background: rgba(0, 0, 0, 0.4);
}

div::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.4);
  border-radius: 0;
  background: rgba(0, 0, 0, 0.2);
}

input {
  border: 1px solid #ccc;
  padding: 7px 0px;
  border-radius: 3px;
  padding-left: 5px;
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075);
  -webkit-transition: border-color ease-in-out .15s, -webkit-box-shadow ease-in-out .15s;
  -o-transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
  transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s
}

input:focus {
  border-color: #66afe9;
  outline: 0;
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, .6);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, .6)
}

select {
  border: 1px solid #ccc;
  padding: 7px 0px;
  border-radius: 3px;
  padding-left: 5px;
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075);
  -webkit-transition: border-color ease-in-out .15s, -webkit-box-shadow ease-in-out .15s;
  -o-transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
  transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s
}

select:focus {
  border-color: #66afe9;
  outline: 0;
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, .6);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(102, 175, 233, .6)
}
</style>