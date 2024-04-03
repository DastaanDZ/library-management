<template>
  <div class="parent">
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
        <form class="d-flex" role="search">
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </nav>
    <div class="main-div">
      <h2>{{ heading }}</h2>
      <div class="cards">
        <Card v-for="(book, index) in books" :key="index" :book="book" />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  name: "ViewAll",
  components: { Card },
  props: {
    books: {
      type: Array,
      required: true,
    },
    heading: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 2rem;
  gap: 2rem;
}
nav {
  width: 100%;
  border-radius: 1rem;
}
nav div {
  display: flex;
  justify-content: center !important ;
}
.d-flex {
  width: 50%;
}
.cards {
  display: flex;
  gap: 2rem;
  width: 100%;
  flex-wrap: wrap;
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
</style>
