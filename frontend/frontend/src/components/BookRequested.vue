<template>
  <div class="main-div">
    <h2>Book Requested</h2>
    <div class="cards">
      <Card />
      <Card />
      <Card />
      <Card />
      <Card />
      <Card />
      <Card />
    </div>
    <h6>
      <a><router-link :to="{ name: 'ViewAll' }">ViewAll</router-link></a>
    </h6>
  </div>
</template>

<script>
import Card from "./Card.vue";
export default {
  name: "BookRequested",
  components: { Card },
};
</script>

<style scoped>
.cards {
  display: flex;
  gap: 2rem;
  width: 100%;
  justify-content: center;
}
.main-div {
  display: flex;
  align-items: start;
  flex-direction: column;
  padding: 2rem;
  background-color: white;
  border-radius: 1rem;
  gap: 1rem;
}
.main-div h6 {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.main-div h6 a {
  cursor: pointer;
  display: flex;
  justify-content: center;
}
.main-div h6 a:hover {
  color: blue;
}
</style>
