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
</style>
